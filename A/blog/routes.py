from flask import render_template, redirect, url_for, flash, request, abort
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, EditProfileFrom, PostForm ,EditPostForm, CommentForm, ReplyForm, LikeForm, DisLikeForm, SearchForm
from blog.models import User, Post, Comment, Reply, Like
from flask_login import login_user, current_user, logout_user, login_required
from flask_dance.contrib.google import google
import jdatetime



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    posts = Post.query.all()
    return render_template('home.html', form=form, posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search_post():
    form = SearchForm()
    search_posts = []
    if form.validate_on_submit():
        title = form.title.data
        search_posts = Post.query.filter(Post.title.contains(title)).all()
    return render_template('home.html', form=form, search_posts=search_posts)

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
        flash('ثبت نام شما با موفقیت انجام شد', 'success')
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
            flash('ورود شما با موفقیت انجام شد', 'success')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است', 'danger')
    return render_template('/login.html', form=form)

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    return f'You are logged in as: {resp.json()["displayName"]}'



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('از حساب خود با موفقیت خارج شدید', 'success')
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
            flash('نام کاری شما حساب شما با موفقیت بروزرسانی شد','info')
            return redirect(url_for('edit_profile'))
    
        elif form.submit_pass.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('رمز عبور حساب شما با موفقیت بروزرسانی شد','info')
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
        flash('پست شما با موفقیت ثبت شد', 'success')
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('create_post.html', form=form)





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
        flash('پست شما با موفقیت تغییر یافت', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit_post.html', form=form)



@app.route('/post_detail/<int:post_id>/', methods=('GET', 'POST'))
@login_required
def post_detail(post_id):

    dislike_form = DisLikeForm()
    like_form = LikeForm()
    comment_form = CommentForm()
    reply_form = ReplyForm()
    post = Post.query.get_or_404(post_id)
    post_date = jdatetime.datetime.fromgregorian(datetime=post.date).strftime('%Y-%m-%d %H:%M')
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if comment_form.validate_on_submit():
        comment = Comment(content=comment_form.content.data, post=post, owner=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('نظر شما با موفقیت شد', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_detail.html', post=post, comment_form=comment_form,
                            reply_form=reply_form ,like_form=like_form, dislike_form=dislike_form,
                              existing_like=existing_like,post_date=post_date)


@app.route('/reply/<int:comment_id>', methods=['GET', 'POST'])
def reply(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment_form = CommentForm()
    reply_form = ReplyForm()
    if reply_form.validate_on_submit():
        reply = Reply(text=reply_form.text.data, comment=comment, response=current_user)
        db.session.add(reply)
        db.session.commit()
        flash('پاسخ شما با موفقیت شد', 'success')
        return redirect(url_for('post_detail', post_id=comment.post.id))
    return render_template('post_detail.html', comment=comment, post=comment.post,
                            comment_form=comment_form, reply_form=reply_form)


@app.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('پست شما با موفقیت حذف شد', 'success')
    return redirect(url_for('home'))


@app.route('/comment/delete/<int:comment_id>')
@login_required
def delete_comment(comment_id):

    comment = Comment.query.get_or_404(comment_id)
    if comment.owner != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('نظر شما با موفقیت حذف شد', 'success')
    return redirect(url_for('home'))


@app.route('/reply/delete/<int:reply_id>')
@login_required
def delete_reply(reply_id):

    reply = Reply.query.get_or_404(reply_id)
    if reply.response != current_user:
        abort(403)
    db.session.delete(reply)
    db.session.commit()
    flash('پاسخ شما با موفقیت حذف شد', 'success')
    return redirect(url_for('home'))


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):

    like_form=LikeForm()
    post = Post.query.get_or_404(post_id)

    if current_user.id:
        existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if not existing_like and like_form.validate_on_submit():
            new_like = Like(user=current_user, like=post)
            db.session.add(new_like)
            db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))

@app.route('/unlike/<int:post_id>', methods=['POST'])
def unlike(post_id):

    dislike_form=DisLikeForm()
    post = Post.query.get_or_404(post_id)

    if current_user.id:
        existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if existing_like and dislike_form.validate_on_submit():
            db.session.delete(existing_like)
            db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    