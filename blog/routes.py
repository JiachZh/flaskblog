
from flask import render_template, url_for, abort
from blog import app
from blog.models import Categories, Posts, Comments, Ratings, Users


@app.route('/')

@app.route("/home")
def home():
    posts = Posts.query.all()
    return render_template('home.html', title='Home', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About Us')

@app.route("/post/<string:post_url>")
def post(post_url):
    post = Posts.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    return render_template('post.html', title=post.title, post=post)