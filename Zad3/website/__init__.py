from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
db_name = "data.db"


def web_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Python'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)
    from .website import website
    app.register_blueprint(website, url_prefix='/')
    from .api import api
    app.register_blueprint(api, url_prefix='/')
    create_db(app)
    return app


def create_db(app):
    if not path.exists('instance/' + db_name):
        with app.app_context():
            db.create_all()
        print('Database initiated!')
