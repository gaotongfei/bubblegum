from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config
from .helpers import time_delta


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.jinja_env.globals.update(time_delta=time_delta)
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .account import bp as account_bp
    app.register_blueprint(account_bp)

    from .nodes import bp as nodes_bp
    app.register_blueprint(nodes_bp)

    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
