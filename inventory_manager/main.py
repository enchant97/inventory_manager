from quart import Quart
from tortoise.contrib.quart import register_tortoise

from .database import models

app = Quart(__name__)


def create_app():
    app.config.from_prefixed_env("IM")

    register_tortoise(
        app,
        db_url=app.config["DB_URI"],
        modules={"models": [models]},
        generate_schemas=True)

    return app
