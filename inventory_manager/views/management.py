from quart import Blueprint, abort, redirect, render_template, request, url_for

from ..database import models
from ..helpers import empty_to_none, none_to_empty, noneable_int

blueprint = Blueprint("management", __name__, url_prefix="/management")


@blueprint.get("/")
async def get_index():
    return await render_template("management/index.jinja")


@blueprint.get("/categories/")
async def get_categories_index():
    roots_count = await models.Category.filter(parent=None, removed_at=None).count()
    total_count = await models.Category.filter(removed_at=None).all().count()
    category_roots = await models.Category.filter(parent=None, removed_at=None).all()

    return await render_template(
        "management/categories/index.jinja",
        roots_count=roots_count,
        total_count=total_count,
        category_roots=category_roots,
    )


@blueprint.get("/categories/<int:category_id>")
async def get_categories_category(category_id: int):
    category = await models.Category.get(id=category_id)
    children = await category.children.filter(removed_at=None).all()

    return await render_template(
        "management/categories/category.jinja",
        category=category,
        children=children,
    )


@blueprint.get("/categories/<int:category_id>/edit")
async def get_categories_category_edit(category_id: int):
    category = await models.Category.get(id=category_id)

    return await render_template(
        "management/categories/edit.jinja",
        category=category,
    )


@blueprint.post("/categories/<int:category_id>/edit")
async def post_categories_category_edit(category_id: int):
    category = await models.Category.get(id=category_id)

    form = await request.form
    category.name = form["name"].strip().lower()
    category.description = empty_to_none(form.get("description"))
    await category.save()

    return redirect(url_for(".get_categories_category_edit", category_id=category_id))


@blueprint.get("/categories/<int:category_id>/purge")
async def get_categories_category_purge(category_id: int):
    await models.Category.filter(id=category_id).delete()

    return redirect(url_for(".get_categories_index"))


@blueprint.get("/categories/new")
async def get_categories_new():
    categories = await models.Category.filter(removed_at=None).all()

    return await render_template(
        "management/categories/new.jinja",
        categories=categories,
    )


@blueprint.post("/categories/new")
async def post_categories_new():
    form = await request.form

    name = form["name"].strip().lower()
    description = empty_to_none(form.get("description"))
    parent_id = empty_to_none(form.get("parent-id"))

    await models.Category.create(
        name=name,
        description=description,
        parent_id=parent_id,
    )

    return redirect(url_for(".get_categories_index"))


@blueprint.get("/locations/")
async def get_locations_index():
    location_roots = await models.Location.filter(parent=None, removed_at=None).all()
    roots_count = await models.Location.filter(parent=None, removed_at=None).count()
    total_count = await models.Location.filter(removed_at=None).all().count()

    return await render_template(
        "management/locations/index.jinja",
        roots_count=roots_count,
        total_count=total_count,
        location_roots=location_roots,
    )


@blueprint.get("/locations/<int:location_id>")
async def get_locations_location(location_id: int):
    location = await models.Location.get(id=location_id)
    children = await location.children.filter(removed_at=None).all()

    return await render_template(
        "management/locations/location.jinja",
        location=location,
        children=children,
    )


@blueprint.get("/locations/<int:location_id>/edit")
async def get_locations_location_edit(location_id: int):
    location = await models.Location.get(id=location_id)

    return await render_template(
        "management/locations/edit.jinja",
        location=location,
    )


@blueprint.post("/locations/<int:location_id>/edit")
async def post_locations_location_edit(location_id: int):
    location = await models.Location.get(id=location_id)

    form = await request.form
    location.name = form["name"].strip().lower()
    location.description = empty_to_none(form.get("description"))
    await location.save()

    return redirect(url_for(".get_locations_location_edit", location_id=location_id))


@blueprint.get("/locations/<int:location_id>/purge")
async def get_locations_location_purge(location_id: int):
    await models.Location.filter(id=location_id).delete()

    return redirect(url_for(".get_locations_index"))


@blueprint.get("/locations/new")
async def get_locations_new():
    locations = await models.Location.filter(removed_at=None).all()

    return await render_template(
        "management/locations/new.jinja",
        locations=locations,
    )


@blueprint.post("/locations/new")
async def post_locations_new():
    form = await request.form

    name = form["name"].strip().lower()
    description = empty_to_none(form.get("description"))
    parent_id = empty_to_none(form.get("parent-id"))

    await models.Location.create(
        name=name,
        description=description,
        parent_id=parent_id,
    )

    return redirect(url_for(".get_locations_index"))


@blueprint.get("/items/")
async def get_items_index():
    recently_added = await models.Item.filter(removed_at=None).all().limit(5).order_by("-created_at")

    return await render_template(
        "management/items/index.jinja",
        recently_added=recently_added,
    )


@blueprint.get("/items/filtered/")
async def get_items_filtered():
    locations = await models.Location.filter(removed_at=None).all()
    categories = await models.Category.filter(removed_at=None).all()

    args = request.args

    row_limit = args.get("row-limit", 10, int)
    if row_limit > 40 or row_limit <= 0:
        abort(400)
    last_id = args.get("last_id")
    name = empty_to_none(args.get("name"))
    category_id = empty_to_none(args.get("category-id"))
    location_id = empty_to_none(args.get("location-id"))
    removed = args.get("removed", False, bool)

    items = models.Item
    filters = {}

    if name:
        filters["name__startswith"] = name
    if category_id:
        filters["category_id"] = category_id
    if location_id:
        filters["location_id"] = location_id
    if last_id:
        filters["id__lt"] = last_id
    if removed:
        filters["removed_at__not_isnull"] = True
    else:
        filters["removed_at"] = None

    items = await items.filter(**filters).all().limit(row_limit).order_by("-id")

    last_item_id = None
    has_next = False
    if len(items) > 0:
        last_item_id = items[-1].id
        next_filters = filters.copy()
        next_filters["id__lt"] = last_item_id
        if await models.Item.filter(**next_filters).order_by("-id").first():
            has_next = True
    next_page_args = args.to_dict()
    next_page_args.pop("last_id", None)

    return await render_template(
        "management/items/filter.jinja",
        locations=locations,
        categories=categories,
        items=items,
        filtered_name=none_to_empty(name),
        filtered_category_id=noneable_int(category_id),
        filtered_location_id=noneable_int(location_id),
        row_limit=row_limit,
        last_item_id=last_item_id,
        next_page_args=next_page_args,
        has_next=has_next,
        removed=removed,
    )


@blueprint.get("/items/<int:item_id>")
async def get_items_item(item_id: int):
    item = await models.Item.get(id=item_id)

    return await render_template(
        "management/items/item.jinja",
        item=item,
    )


@blueprint.get("/items/<int:item_id>/edit")
async def get_items_item_edit(item_id: int):
    item = await models.Item.get(id=item_id)
    categories = await models.Category.filter(removed_at=None).all()
    locations = await models.Location.filter(removed_at=None).all()

    return await render_template(
        "management/items/edit.jinja",
        item=item,
        categories=categories,
        locations=locations,
    )


@blueprint.post("/items/<int:item_id>/edit")
async def post_items_item_edit(item_id: int):
    item = await models.Item.get(id=item_id)

    form = await request.form
    item.name = form["name"].strip().lower()
    item.description = empty_to_none(form.get("description"))
    item.expires = empty_to_none(form.get("expiry"))
    item.quantity = int(form["quantity"])
    item.category_id = int(form["category-id"])
    item.location_id = int(form["location-id"])
    await item.save()

    return redirect(url_for(".get_items_item_edit", item_id=item.id))


@blueprint.get("/items/<int:item_id>/purge")
async def get_items_item_purge(item_id: int):
    await models.Item.filter(id=item_id).delete()

    return redirect(url_for(".get_items_index", item_id=item_id))


@blueprint.get("/items/new")
async def get_items_new():
    categories = await models.Category.filter(removed_at=None).all()
    locations = await models.Location.filter(removed_at=None).all()

    return await render_template(
        "management/items/new.jinja",
        categories=categories,
        locations=locations,
    )


@blueprint.post("/items/new")
async def post_items_new():
    form = await request.form

    name = form["name"].strip().lower()
    description = empty_to_none(form.get("description"))
    expires = empty_to_none(form.get("expiry"))
    quantity = form["quantity"]
    category_id = form["category-id"]
    location_id = form["location-id"]

    await models.Item.create(
        name=name,
        description=description,
        expires=expires,
        quantity=quantity,
        category_id=category_id,
        location_id=location_id,
    )

    return redirect(url_for(".get_items_index"))
