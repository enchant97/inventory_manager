from quart import Blueprint, render_template

blueprint = Blueprint("manage", __name__, url_prefix="/manage")


@blueprint.get("/")
async def get_index():
    return await render_template("manage/index.jinja")
