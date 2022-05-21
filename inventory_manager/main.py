from quart import Quart
from tortoise.contrib.quart import register_tortoise

from .database import models
from .helpers import COL_NAMES_TO_HUMAN
from .views import management, report, root

app = Quart(__name__)


def create_app():
    app.config.from_prefixed_env("IM")
    if app.config["ROW_LIMIT"] <= 0:
        raise ValueError("Row limit cannot be less than 1")
    app.config["COL_NAMES_TO_HUMAN"] = COL_NAMES_TO_HUMAN

    app.register_blueprint(management.blueprint)
    app.register_blueprint(report.blueprint)
    app.register_blueprint(root.blueprint)

    register_tortoise(
        app,
        db_url=app.config["DB_URI"],
        modules={"models": [models]},
        generate_schemas=True)

    return app
