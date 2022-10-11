from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# database management
# using sql alchemy

import config

db = SQLAlchemy()
migrate = Migrate()


# application factory
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # configur database
    # using ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    
    # bluprint
    from .views import main_views
    app.register_blueprint(main_views.blueprint)

    return app
