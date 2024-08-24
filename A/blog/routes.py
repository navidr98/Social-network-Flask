from flask import render_template, redirect, url_for, flash, request
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, EditProfileFrom
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        next_page = request.args.get('next')
        flash('You registered successfully', 'success')
        return redirect(next_page if next_page else url_for('home'))
    return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('You logged in successfully', 'success')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('Email or Password is wrong', 'danger')
    return render_template('/login.html', form=form)


@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('You logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():

    form = EditProfileFrom()

    if form.validate_on_submit():
        if form.submit_user.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your profile has been updated','info')
            return redirect(url_for('profile'))
    
        elif form.submit_pass.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated','info')
            return redirect(url_for('profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', form=form)

    








