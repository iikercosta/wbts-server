from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from web.api.controller.devices import devices

    app.register_blueprint(views, url_prefic="/")
    app.register_blueprint(devices, url_prefix='/')

    from web.api.model.models import Location, Device, Timestamp

    create_database(app)

    return app


def create_database(app):
    if not path.exists('web/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
