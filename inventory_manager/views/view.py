from quart import Blueprint, render_template

from ..database import models

blueprint = Blueprint("view", __name__, url_prefix="/view")


@blueprint.get("/")
async def get_index():
    return await render_template("view/index.jinja")


@blueprint.get("/categories/")
async def get_categories_index():
    category_roots = await models.Category.filter(parent=None).all()

    return await render_template(
        "view/categories/index.jinja",
        category_roots=category_roots,
    )


@blueprint.get("/categories/<int:category_id>")
async def get_categories_category(category_id: int):
    category = await models.Category.get(id=category_id)
    children = await category.children.all()

    return await render_template(
        "view/categories/category.jinja",
        category=category,
        children=children,
    )


@blueprint.get("/locations/")
async def get_locations_index():
    location_roots = await models.Location.filter(parent=None).all()

    return await render_template(
        "view/locations/index.jinja",
        location_roots=location_roots,
    )


@blueprint.get("/locations/<int:location_id>")
async def get_locations_location(location_id: int):
    location = await models.Location.get(id=location_id)
    children = await location.children.all()

    return await render_template(
        "view/locations/location.jinja",
        location=location,
        children=children,
    )
