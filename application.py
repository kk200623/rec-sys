from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .views import main_bp


login_database = SQLAlchemy() ## initialize a new database
login_manager= LoginManager()

def create_app(): #config_file='flask_config.py'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aklsfjlaksjdi8uiii390oll'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///tmp/test.db"
    login_database.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        login_database.create_all()

    app.register_blueprint(main_bp)

    return app
