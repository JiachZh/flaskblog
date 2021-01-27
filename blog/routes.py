
from flask import render_template, url_for, abort, request, redirect
from blog import app, db
from blog.models import Categories, Posts, Comments, Ratings, Users
from blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user


@app.route('/')

@app.route('/home')
def home():
    posts = Posts.query.all()
    return render_template('home.html', title='Home', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/post/<string:post_url>')
def post(post_url):
    post = Posts.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    return render_template('post.html', title=post.title, post=post)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user = Users(firstName=form.firstName.data, lastName=form.lastName.data,email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))