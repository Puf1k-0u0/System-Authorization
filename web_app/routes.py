from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from web_app import app, db
from web_app.models import User


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not (username or password or password2):
            flash('Fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        elif db.session.query(User).filter_by(username=username).first() is not None:
            flash('This username is taken! Choose another username.')
        else:
            hash_password = generate_password_hash(password)
            new_user = User(username=username, password=hash_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('authorization'))

    return render_template('registration.html')

@app.route("/web_app", methods=["GET", "POST"])
def authorization():
    user = current_user.get_id()
    if user is not None:
        flash('You must logout before authorization!')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        next_page = request.args.get('next')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                if next_page is not None:
                    return redirect(next_page)
                else:
                    return redirect(url_for('profile'))
            else:
                flash('Username or password is not correct!')
        else:
            flash('Fill username and password fields!')

    return render_template('auth.html')

@app.route("/quit", methods=["GET", "POST"])
@login_required
def quit():
    logout_user()
    next_page = request.args.get('next')
    if next_page is not None:
        return redirect(next_page)
    else:
        return redirect(url_for('main'))

@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('authorization') + '?next=' + request.url)
    return response

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    user_id = current_user.get_id()
    user = db.session.query(User).get(user_id)
    username = user.username
    return render_template('profile.html', username=username)

@app.route("/admin-panel", methods=["GET"])
@login_required
def admin_panel():
    user = current_user.get_id()
    user = db.session.query(User).get(user)
    if user.username == "admin" and user.id == 1:
        users = db.session.query(User).all()
        return render_template('admin-panel.html', users=users)
    else:
        return redirect(url_for('main'))

@app.route("/delete-user/<int:id>", methods=["GET", "POST"])
def delete_user(id):
    admin = current_user.get_id()
    if admin is None:
        return redirect(url_for('main'))

    admin = db.session.query(User).get(admin)
    if admin.username == "admin" and admin.id == 1:
        user = db.session.query(User).get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        return redirect(url_for('admin_panel'))
    else:
        return redirect(url_for('main'))
