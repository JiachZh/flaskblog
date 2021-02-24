from flask import render_template, url_for, abort, request, redirect, flash
from blog import app, db
from blog.models import Categories, Posts, Comments, Ratings, Users
from blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required
from sqlalchemy.sql import func

@app.route('/')
@app.route('/home')
def home():
    posts = Posts.query.all()
    return render_template('home.html', title='Home', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/allposts', methods=['GET'])
def allposts():
    posts = Posts.query.all()
    return render_template('allposts.html', title='All posts', posts=posts)

@app.route('/post/<string:post_url>')
def post(post_url):
    post = Posts.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    comments = Comments.query.filter_by(postId=post.postId).join(Users)
    ratings = Ratings.query.filter_by(postId=post.postId).with_entities(func.avg(Ratings.content).label('average'))
    return render_template('post.html', title=post.title, post=post, comments=comments, ratings=ratings)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(userName=form.userName.data, firstName=form.firstName.data, lastName=form.lastName.data,email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email address or password.')
    return render_template('login.html', title='Login', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('about.html', title='About Us')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
