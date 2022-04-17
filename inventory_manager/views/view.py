from quart import Blueprint, abort, render_template, request

from ..database import models
from ..helpers import empty_to_none, none_to_empty, noneable_int

blueprint = Blueprint("view", __name__, url_prefix="/view")


@blueprint.get("/")
async def get_index():
    return await render_template("view/index.jinja")


@blueprint.get("/categories/")
async def get_categories_index():
    category_roots = await models.Category.filter(parent=None, removed_at=None).all()

    return await render_template(
        "view/categories/index.jinja",
        category_roots=category_roots,
    )


@blueprint.get("/categories/<int:category_id>")
async def get_categories_category(category_id: int):
    category = await models.Category.get(id=category_id)
    children = await category.children.filter(removed_at=None).all()

    return await render_template(
        "view/categories/category.jinja",
        category=category,
        children=children,
    )


@blueprint.get("/locations/")
async def get_locations_index():
    location_roots = await models.Location.filter(parent=None, removed_at=None).all()

    return await render_template(
        "view/locations/index.jinja",
        location_roots=location_roots,
    )


@blueprint.get("/locations/<int:location_id>")
async def get_locations_location(location_id: int):
    location = await models.Location.get(id=location_id)
    children = await location.children.filter(removed_at=None).all()

    return await render_template(
        "view/locations/location.jinja",
        location=location,
        children=children,
    )


@blueprint.get("/items/")
async def get_items_index():
    recently_added = await models.Item.filter(removed_at=None).all().limit(5).order_by("-created_at")

    return await render_template(
        "view/items/index.jinja",
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

    items = await items.filter(**filters, removed_at=None).all().limit(row_limit).order_by("-id")

    last_item_id = None
    has_next = False
    if len(items) > 0:
        last_item_id = items[-1].id
        next_filters = filters.copy()
        next_filters["id__lt"] = last_item_id
        if await models.Item.filter(**next_filters, removed_at=None).order_by("-id").first():
            has_next = True
    next_page_args = args.to_dict()
    next_page_args.pop("last_id", None)

    return await render_template(
        "view/items/filter.jinja",
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
    )


@blueprint.get("/items/<int:item_id>")
async def get_items_item(item_id: int):
    item = await models.Item.get(id=item_id)

    return await render_template(
        "view/items/item.jinja",
        item=item,
    )
