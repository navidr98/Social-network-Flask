from flask import render_template, redirect, url_for, flash
from blog import app, db
from blog.forms import RegistrationForm, LoginForm
from blog.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    flash('You registered successfully', 'success')
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You registered successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    
    return render_template('/login.html', form=form)




