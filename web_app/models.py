from flask_login import UserMixin

from web_app import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
