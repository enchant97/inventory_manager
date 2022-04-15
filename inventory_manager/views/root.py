from quart import Blueprint, render_template

blueprint = Blueprint("root", __name__)


@blueprint.get("/")
async def get_index():
    return await render_template("root/index.jinja")
