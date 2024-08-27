from flask import render_template, redirect, url_for, flash, request, abort
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, EditProfileFrom, PostForm ,EditPostForm, CommentForm, ReplyForm
from blog.models import User, Post, Comment, Reply
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

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


@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@app.route('/profile/edit/>', methods=['GET','POST'])
def edit_profile():
    form = EditProfileFrom()

    if form.validate_on_submit():
        if form.submit_user.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your profile has been updated','info')
            return redirect(url_for('edit_profile'))
    
        elif form.submit_pass.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated','info')
            return redirect(url_for('edit_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)


 
@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post created successfully', 'success')
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('create_post.html', form=form)



@app.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('home'))


@app.route('/post/update/<int:post_id>', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form = EditPostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit_post.html', form=form)



@app.route('/post_detail/<int:post_id>/', methods=('GET', 'POST'))
@login_required
def post_detail(post_id):
    form = CommentForm()
    form_rep = ReplyForm()
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(post_id)
    if form.validate_on_submit() and form.submit.data:
        comment = Comment(content=form.content.data, post=post, owner=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment added successfully', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
        
    elif form_rep.validate_on_submit() and form_rep.submit_reply.data:
        reply = Reply(text=form_rep.text.data, rep=comment, response=current_user)
        db.session.add(reply)
        db.session.commit()
        flash('Your reply added successfully', 'success')
        return redirect(url_for('post_detail', post_id=post.id,))

    return render_template('post_detail.html', post=post, form=form, form_rep=form_rep)
