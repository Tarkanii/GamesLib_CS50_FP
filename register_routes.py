from flask import render_template
from flask_login import current_user
from . import MESSAGE_404, MESSAGE_500
from .auth_routes import auth
from .main_routes import main

def register_routes(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error-page.html", user = current_user, message = MESSAGE_404)

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("error-page.html", user = current_user, message = MESSAGE_500)
    
    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(main, url_prefix = "/")
