from flask import Blueprint, request, make_response, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html", user = current_user)

@main.route("/my-library")
@login_required
def my_library():
    return render_template("my-library.html", user = current_user)