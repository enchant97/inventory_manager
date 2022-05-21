from datetime import date, timedelta

from quart import Blueprint, abort, redirect, render_template, request, url_for

from ..database import models
from ..helpers import empty_to_none

blueprint = Blueprint("report", __name__, url_prefix="/report")


@blueprint.get("/")
async def get_index():
    reports = await models.ItemReport.filter(removed_at=None).all()
    return await render_template(
        "report/index.jinja",
        reports=reports,
    )


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


@blueprint.get("/<int:report_id>")
async def get_report(report_id: int):
    report = await models.ItemReport.get(id=report_id)

    requested_cols = ["id", "name"]
    current_date = date.today()
    warning_date = current_date + timedelta(days=6)

    if report.show_description:
        requested_cols.append("description")
    if report.show_expiry:
        requested_cols.append("expires")
    if report.show_location:
        requested_cols.append("location__name")
    if report.show_category:
        requested_cols.append("category__name")

    items = models.Item.filter(removed_at=None)
    if report.filter_expired_only:
        items = items.filter(expires__lt=current_date)

    match report.sort_mode:
        case models.ReportSortTypes.CREATION:
            items = items.order_by("created_at")
        case models.ReportSortTypes.CREATION_DESC:
            items = items.order_by("-created_at")
        case models.ReportSortTypes.EXPIRY:
            items = items.order_by("expires")
        case models.ReportSortTypes.EXPIRY_DESC:
            items = items.order_by("-expires")

    items = await items.values(*requested_cols)
    # remove the id as "humans" should not be looking at that
    requested_cols.pop(0)

    return await render_template(
        "report/report.jinja",
        report=report,
        items=items,
        requested_cols=requested_cols,
        current_date=current_date,
        warning_date=warning_date,
        )


@blueprint.get("/<int:report_id>/purge")
async def get_purge(report_id: int):
    await models.ItemReport.filter(id=report_id).delete()
    return redirect(url_for(".get_index"))
