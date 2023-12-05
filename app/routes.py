from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app.models import User
from app import app, db
from app.forms import LoginForm, RegistrationForm
from urllib.parse import urlsplit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

#try getting working without modules first
#if working, then modularize
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('profile')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/signup.html', title='Register', form=form)

@app.route('/profile')
@login_required
def profile():
    #change me to non-hardcoded later
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('profile.html', title='Profile Page', posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
