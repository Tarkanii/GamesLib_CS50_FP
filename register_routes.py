from .auth_routes import auth
from .main_routes import main

def register_routes(app):
    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(main, url_prefix = "/")
