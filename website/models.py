from .create_app import db
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key = True, nullable = False)
    email = db.Column("email", db.Text, nullable = False, unique = True)
    hash_password = db.Column("hash_password", db.Text, nullable = False)
    gm = db.relationship("Game")
    games = association_proxy("gm", "game_id")

    def __init__(self, email, password):
        self.email = email
        self.hash_password = password

    def __repr__(self):
        return f"User with id: {self.id}, email: {self.email}, games: {self.games}"
    
class Game(db.Model):
    __tablename__ = "games"

    id = db.Column("id", db.Integer, primary_key = True, nullable = False)
    game_id = db.Column("game_id", db.Integer, nullable = False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, game_id, user_id):
        self.game_id = game_id
        self.user_id = user_id

    def __repr__(self):
        return f"{self.game_id}, {self.id}, {self.user_id}"