from quart import Blueprint, render_template, request

from ..database import models
from ..helpers import empty_to_none, none_to_empty

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
    recently_added = await models.Item.filter(removed_at=None).all().limit(5)

    return await render_template(
        "view/items/index.jinja",
        recently_added=recently_added,
    )


@blueprint.get("/items/filtered/")
async def get_items_filtered():
    locations = await models.Location.filter(removed_at=None).all()
    categories = await models.Category.filter(removed_at=None).all()

    args = request.args

    name = empty_to_none(args.get("name"))
    category_id = empty_to_none(args.get("category-id"))
    location_id = empty_to_none(args.get("location-id"))
    removed = args.get("removed", bool, False)

    items = models.Item
    filters = {}

    if name:
        filters["name__startswith"] = name
    if category_id:
        filters["category_id"] = category_id
    if location_id:
        filters["location_id"] = location_id

    items = await items.filter(**filters, removed_at=None).all()

    return await render_template(
        "view/items/filter.jinja",
        locations=locations,
        categories=categories,
        items=items,
        filtered_name=none_to_empty(name),
        filtered_category_id=none_to_empty(category_id),
        filtered_location_id=none_to_empty(location_id),
    )
