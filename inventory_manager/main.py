import logging

from quart import Quart
from tortoise.contrib.quart import register_tortoise

from .database import models
from .helpers import COL_NAMES_TO_HUMAN
from .views import management, report, root

app = Quart(__name__)


def create_app():
    # load config
    app.config.from_prefixed_env("IM")

    # Load human names for db columns
    app.config["COL_NAMES_TO_HUMAN"] = COL_NAMES_TO_HUMAN

    # set custom row limit for displaying results
    if (row_limit := app.config.get("ROW_LIMIT", "15")):
        app.config["ROW_LIMIT"] = int(row_limit)
        if app.config["ROW_LIMIT"] <= 0:
            # ensure row-limit is positive value
            raise ValueError("Row limit cannot be less than 1")

    # allow for custom log level to be set
    if (log_level := app.config.get("LOG_LEVEL")) is not None:
        log_level = logging.getLevelName(log_level.upper())
        app.logger.setLevel(log_level)

    # register app blueprints
    app.register_blueprint(management.blueprint)
    app.register_blueprint(report.blueprint)
    app.register_blueprint(root.blueprint)

    # register the database and generate schemas if not already created
    register_tortoise(
        app,
        db_url=app.config["DB_URI"],
        modules={"models": [models]},
        generate_schemas=True)

    return app
