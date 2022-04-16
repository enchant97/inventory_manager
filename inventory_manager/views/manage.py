from quart import Blueprint, redirect, render_template, request, url_for

from ..database import models
from ..helpers import empty_to_none

blueprint = Blueprint("manage", __name__, url_prefix="/manage")


@blueprint.get("/")
async def get_index():
    return await render_template("manage/index.jinja")


@blueprint.get("/categories/")
async def get_categories_index():
    roots_count = await models.Category.filter(parent=None, removed_at=None).count()
    total_count = await models.Category.filter(removed_at=None).all().count()

    return await render_template(
        "manage/categories/index.jinja",
        roots_count=roots_count,
        total_count=total_count,
    )


@blueprint.get("/categories/new")
async def get_categories_new():
    categories = await models.Category.filter(removed_at=None).all()

    return await render_template(
        "manage/categories/new.jinja",
        categories=categories,
    )


@blueprint.post("/categories/new")
async def post_categories_new():
    form = await request.form

    name = form["name"].strip().lower()
    description = empty_to_none(form.get("description"))
    parent_id = empty_to_none(form.get("parent-id"))

    category = await models.Category.create(
        name=name,
        description=description,
        parent_id=parent_id,
    )

    return redirect(url_for(".get_categories_index"))


@blueprint.get("/locations/")
async def get_locations_index():
    roots_count = await models.Location.filter(parent=None, removed_at=None).count()
    total_count = await models.Location.filter(removed_at=None).all().count()

    return await render_template(
        "manage/locations/index.jinja",
        roots_count=roots_count,
        total_count=total_count,
    )


@blueprint.get("/locations/new")
async def get_locations_new():
    locations = await models.Location.filter(removed_at=None).all()

    return await render_template(
        "manage/locations/new.jinja",
        locations=locations,
    )


@blueprint.post("/locations/new")
async def post_locations_new():
    form = await request.form

    name = form["name"].strip().lower()
    description = empty_to_none(form.get("description"))
    parent_id = empty_to_none(form.get("parent-id"))

    location = await models.Location.create(
        name=name,
        description=description,
        parent_id=parent_id,
    )

    return redirect(url_for(".get_locations_index"))


@blueprint.get("/items/")
async def get_items_index():
    return await render_template("manage/items/index.jinja")


@blueprint.get("/items/new")
async def get_items_new():
    categories = await models.Category.filter(removed_at=None).all()
    locations = await models.Location.filter(removed_at=None).all()

    return await render_template(
        "manage/items/new.jinja",
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
