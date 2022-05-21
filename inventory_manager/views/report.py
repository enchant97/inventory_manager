from quart import Blueprint, abort, redirect, render_template, request, url_for

from ..database import models
from ..helpers import empty_to_none

blueprint = Blueprint("report", __name__, url_prefix="/report")


@blueprint.get("/")
async def get_index():
    return await render_template("report/index.jinja")


@blueprint.get("/new")
async def get_new():
    categories = await models.Category.filter(removed_at=None).all()
    locations = await models.Location.filter(removed_at=None).all()
    return await render_template(
        "report/new.jinja",
        categories=categories,
        locations=locations,
    )


@blueprint.post("/new")
async def post_new():
    form = await request.form

    name = form["name"].strip().lower()
    filter_location = empty_to_none(form["location"])
    filter_category = empty_to_none(form["category"])
    filter_expired_only = form.get("expired-only", False, bool)
    sort_mode = empty_to_none(form["sort-method"])
    if sort_mode is not None:
        sort_mode = models.ReportSortTypes(sort_mode)
    show_description = form.get("show-description", False, bool)
    show_expiry = form.get("show-expiry", False, bool)
    show_location = form.get("show-location", False, bool)
    show_category = form.get("show-category", False, bool)
    show_quick_actions = form.get("show-quick-actions", False, bool)

    await models.ItemReport.create(
        name=name,
        filter_location_id=filter_location,
        filter_category_id=filter_category,
        filter_expired_only=filter_expired_only,
        sort_mode=sort_mode,
        show_description=show_description,
        show_expiry=show_expiry,
        show_location=show_location,
        show_category=show_category,
        show_quick_actions=show_quick_actions,
    )

    return redirect(url_for(".get_index"))
