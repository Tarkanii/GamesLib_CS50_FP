from flask import Blueprint, request, make_response, render_template, redirect, session
from re import fullmatch
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from . import MESSAGE_500

auth = Blueprint("auth", __name__)

EMAIL_REGEX = r'^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/my-library")
    
    if request.method == "POST":
        email = str(request.form["email"]).replace(" ", "")
        password = request.form["password"]
        hints = {}

        if not email or not fullmatch(EMAIL_REGEX, email):
            hints["email"] = "Please provide correct email"

        if not password:
            hints["password"] = "Please provide your password"
        
        if "email" in hints or "password" in hints:
            return render_template("login.html", user = current_user, hints = hints, email = email)

        try:
            user = User.query.filter(User.email == email).first()
            if not user:
                hints["password"] = "Wrong email or password!"
                return render_template("login.html", user = current_user, hints = hints, email = email)

            if not check_password_hash(user.hash_password, password):
                hints["password"] = "Wrong email or password!"
                return render_template("login.html", user = current_user, hints = hints, email = email)

            login_user(user, remember=True)
        except SQLAlchemyError:
            return render_template("error-page.html", user = current_user, message = MESSAGE_500)

        return redirect("/my-library")
    else:
        return render_template("login.html", user = current_user, hints = {}, email = "")
    
@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/my-library")

    if request.method == "POST":
        email = str(request.form["email"]).replace(" ", "")
        password = request.form["password"]
        confirmation = request.form["confirmation"]
        hints = {}
        values = {
            "email": email,
            "password": password,
            "confirmation": confirmation
        }

        if not email or not fullmatch(EMAIL_REGEX, email):
            hints["email"] = "Please provide correct email"
        
        if not password or len(password) < 8 or password.find(" ") != -1:
            hints["password"] = "Password min length is 8 characters, no spaces"
        
        if not confirmation or password != confirmation:
            hints["confirmation"] = "Passwords should match"

        if "email" in hints or "password" in hints or "confirmation" in hints:
            return render_template("signup.html", user = current_user, hints = hints, values = values)

        try:
            same_users = User.query.filter(User.email == email).all()
            if len(same_users) > 0:
                hints["confirmation"] = "Email is already registered"
                return render_template("signup.html", user = current_user, hints = hints, values = values)

            user = User(email, generate_password_hash(password, salt_length = 16))
            db.session.add(user)
            db.session.commit()

            login_user(user, remember = True)
        except SQLAlchemyError:
            return render_template("error-page.html", user = current_user, message = MESSAGE_500)
        
        return redirect("/my-library")
    else:
        return render_template("signup.html", user = current_user, hints = {}, values = {"email": "", "password": "", "confirmation": ""})
    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")