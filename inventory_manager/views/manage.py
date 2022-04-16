from quart import Blueprint, render_template, redirect, url_for, request

from ..database import models

blueprint = Blueprint("manage", __name__, url_prefix="/manage")


@blueprint.get("/")
async def get_index():
    return await render_template("manage/index.jinja")


@blueprint.get("/categories/")
async def get_categories_index():
    roots_count = await models.Category.filter(parent=None).count()
    total_count = await models.Category.all().count()

    return await render_template(
        "manage/categories/index.jinja",
        roots_count=roots_count,
        total_count=total_count,
    )


@blueprint.get("/categories/new")
async def get_categories_new():
    categories = await models.Category.all()

    return await render_template(
        "manage/categories/new.jinja",
        categories=categories,
    )


@blueprint.post("/categories/new")
async def post_categories_new():
    form = await request.form

    name = form["name"].strip().lower()
    description = form.get("description")
    if description == "":
        description = None
    parent_id = form.get("parent-id")
    if parent_id == "":
        parent_id = None

    category = await models.Category.create(
        name=name,
        description=description,
        parent_id=parent_id,
    )

    return redirect(url_for(".get_categories_index"))
