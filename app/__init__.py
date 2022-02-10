from flask import Flask
from flask import app as app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="templates/")

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    global socketio
    socketio = SocketIO(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for admin routes in our app
    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    # blueprint for manager routes in our app
    from .manager import manager_blueprint
    app.register_blueprint(manager_blueprint)

    return app

