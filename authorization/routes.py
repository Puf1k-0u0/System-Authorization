from flask import render_template

from authorization import app


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")