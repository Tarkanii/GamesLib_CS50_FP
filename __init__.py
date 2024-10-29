from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.exc import SQLAlchemyError

MESSAGE_500 = "500 Internal issue, try again later"
MESSAGE_404 = "404 Page not found"

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = "DSFSFSDFSDFSDFSFSW"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://MainUser:mainuserpassword@localhost/GamesLibCS50"
    
    from .register_routes import register_routes
    register_routes(app)
    
    db.init_app(app)
    
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    from .models import User
    @login_manager.user_loader
    def load_user(id):
        try:
            return User.query.get(int(id))
        except SQLAlchemyError as e:
            return None
    
    return app