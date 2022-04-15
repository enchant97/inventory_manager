from quart import Quart
from tortoise.contrib.quart import register_tortoise

from .database import models
from .views import manage, root, view

app = Quart(__name__)


def create_app():
    app.config.from_prefixed_env("IM")

    app.register_blueprint(manage.blueprint)
    app.register_blueprint(root.blueprint)
    app.register_blueprint(view.blueprint)

    register_tortoise(
        app,
        db_url=app.config["DB_URI"],
        modules={"models": [models]},
        generate_schemas=True)

    return app
