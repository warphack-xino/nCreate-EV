from hack import app,db
from flask import render_template,redirect,url_for,request,flash,abort
from flask_login import login_user,login_required,logout_user,current_user
from hack.models import User
from hack.forms import LoginForm
from sqlalchemy import desc , asc
from werkzeug.security import generate_password_hash,check_password_hash
import flask
from datetime import datetime
@app.route('/')
def home():
    return render_template('HomePage.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    mess = 'Please fill the form to login to your account.'
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully.", category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            mess = "Email not found"

    return render_template('Login.html', mess=mess)

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    mess = 'Please fill the form to create an account.'
    if request.method == 'POST':
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            mess = 'Email already exists.'
        elif password1 != password2:
            mess = "Passwords don't match"
        elif len(password1) < 6:
            mess = 'Password is too short'
        elif len(email) < 4:
            mess = 'Invalid email'
        else:
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('home'))

    return render_template('reg.html', mess=mess)

@app.route('/cart')
@login_required
def cart():
    return "<h1> This is the cart page. </h1>"



if __name__ == '__main__':
    app.run(debug=True)
