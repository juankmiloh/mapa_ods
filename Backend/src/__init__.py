
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
from flask_cors import CORS
from injector import Module, Injector, singleton
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from .service import ServiceModule
from .repository import RepositoryModule

il = logging.getLogger('injector')
il.addHandler(logging.StreamHandler())
il.level = logging.DEBUG

Base = declarative_base()


class AppModule(Module):
    def __init__(self, db, postgresdb):
        self.db = db
        self.postgresdb = postgresdb

    def configure(self, binder):
        binder.bind(SQLAlchemy, to=self.db, scope=singleton)


def create_app():

    config_name = os.environ.get('FLASK_ENV', 'production')
    app = Flask(__name__,
                static_folder="../front/dist/static",
                template_folder="../front/dist"
                )
    app.config.from_object('config_' + config_name)

    postgresdb = create_engine(app.config.get("SQLALCHEMY_DATABASE_POSTGRES_URI")).connect()

    db = SQLAlchemy()
    db.init_app(app)

    injector = Injector([AppModule(db, postgresdb), RepositoryModule(db, postgresdb), ServiceModule()])

    from .controller import controller as controller_blueprint
    app.register_blueprint(controller_blueprint)

    if app.config.get("ENV") == 'development' or app.config.get("ENV") == 'production':
        CORS(app, resources={
             r"*": {"origins": "*", "supports_credentials": True}})

    FlaskInjector(app=app, injector=injector)

    return app
