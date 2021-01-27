
from flask import render_template, url_for
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
