from quart import Blueprint, render_template

blueprint = Blueprint("view", __name__, url_prefix="/view")


@blueprint.get("/")
async def get_index():
    return await render_template("view/index.jinja")
