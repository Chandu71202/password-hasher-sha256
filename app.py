from myproject import app,db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    flash("Hi hello")
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!',category='success')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data) is not None:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return render_template('home.html')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        email=form.email.data
        username=form.username.data
        password=form.password.data
        pass_confirm = form.pass_confirm.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != pass_confirm:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'))
            flash('Thanks for registering! Now you can login!',category='success')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return redirect(url_for('register'))
  
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
