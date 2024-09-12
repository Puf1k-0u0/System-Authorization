from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/sys_auth'
db = SQLAlchemy(app)

#manager = LoginManager(app)

from authorization import models, routes
