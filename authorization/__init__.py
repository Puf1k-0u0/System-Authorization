from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.app_context().push()
app.secret_key = 'system auth salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/sys_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)

from authorization import models, routes

db.create_all()
