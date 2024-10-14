from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key = True, nullable = False)
    email = db.Column("email", db.Text, nullable = False)
    hash_password = db.Column("hash_password", db.Text, nullable = False)

    def __init__(self, email, password):
        self.email = email
        self.hash_password = password

    def __repr__(self):
        return f"User with id: {self.id}, email: {self.email}, password: {self.hash_password}"