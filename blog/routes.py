from flask import render_template, url_for, abort, request, redirect, flash, jsonify
from blog import app, db
from blog.models import Posts, Comments, Ratings, Users, Taggings
from blog.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.sql import func
from datetime import datetime

@app.route('/')
@app.route('/home')
def home():
    posts = Posts.query.filter_by(listed=1).order_by(Posts.pinned.desc(), Posts.createdAt.desc()).add_column(func.avg(Ratings.content).label('avg_rating')).join(Ratings, Ratings.postId==Posts.postId, isouter=True).group_by(Posts.postId).limit(12).all()
    return render_template('home.html', title='Home', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/allposts', methods=['GET'])
def allposts():
    posts = Posts.query.filter_by(listed=1).order_by(Posts.createdAt.desc()).add_column(func.avg(Ratings.content).label('avg_rating')).join(Ratings, Ratings.postId==Posts.postId, isouter=True).group_by(Posts.postId).all()
    return render_template('allposts.html', title='All posts', posts=posts)

@app.route('/search')
def search():
    # TODO: Clumsy implementation of search engine, needs to be improved
    posts = Posts.query.filter_by(listed=1).all()
    print(request.args.get('keywords'))
    return render_template('search.html', title='Search results', posts=posts, keywords=request.args.get('keywords'))

@app.route('/post/<string:post_url>')
def post(post_url):
    post = Posts.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    comments = Comments.query.filter_by(postId=post.postId)
    rating = Ratings.query.filter_by(postId=post.postId).with_entities(func.avg(Ratings.content).label('average')).first()
    if current_user.is_authenticated:
        my_rating = Ratings.query.filter_by(postId=post.postId, authorId=current_user.userId).first()
        tagged = Taggings.query.filter_by(postId=post.postId, authorId=current_user.userId).first()
    else:
        my_rating = None
        tagged = None
    return render_template('post.html', title=post.title, post=post, comments=comments, rating=rating, my_rating=my_rating, tagged=tagged)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(userName=form.userName.data, firstName=form.firstName.data, lastName=form.lastName.data,email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration success! ')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Logged in successfully! ')
            return redirect(url_for('home'))
        else:
            flash('Invalid email address or password.')
    return render_template('login.html', title='Login', form=form)

@app.route('/profile')
@login_required
def profile():
    taggings = Taggings.query.filter_by(authorId=current_user.userId).order_by(Taggings.createdAt.desc()).all()
    return render_template('profile.html', title='Tagged posts', taggings=taggings)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully! ')
    return redirect(url_for('home'))

@app.route('/edit/<string:post_url>', methods=['GET', 'POST'])
@login_required
def edit(post_url):
    if current_user.userName != 'admin':
        abort(401)
        pass
    post = Posts.query.filter_by(url=post_url).first()
    if request.method == 'GET':
        return render_template('editor.html', title='editor', post=post)
    if post is None:
        post = Posts(
            url=post_url, 
            title=request.form.get('Title'),
            content=request.form.get('Content'),
            image=request.form.get('Image'),
            hidden=request.form.get('Hidden'),
            listed=request.form.get('Listed'),
            pinned=request.form.get('Pinned')
        )
        db.session.add(post)
    else:
        if request.form.get('Delete'):
            post.hidden = 1
        else:
            post.title = request.form.get('Title')
            post.content = request.form.get('Content')
            post.image = request.form.get('Image')
            post.hidden = request.form.get('Hidden')
            post.listed = request.form.get('Listed')
            post.pinned = request.form.get('Pinned')
        post.updatedAt = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'Success'})

@app.route('/comment', methods=['POST'])
@login_required
def comment():
    commentId = request.form.get('CommentId')
    if commentId is None:
        comment = Comments(content=request.form.get('Content'), postId=request.form.get('PostId'), authorId=current_user.get_id())
        db.session.add(comment)
    else:
        comment = Comments.query.filter_by(authorId=current_user.userId, commentId=commentId).first()
        if request.form.get('Delete'):
            db.session.delete(comment)
        else:
            comment.content = request.form.get('Content')
            comment.updatedAt = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'Success'})

@app.route('/rating', methods=['POST'])
@login_required
def rating():
    rating = Ratings.query.filter_by(authorId=current_user.get_id(), postId=request.form.get('PostId')).first()
    if rating is None:
        rating = Ratings(content=request.form.get('Content'), postId=request.form.get('PostId'), authorId=current_user.get_id())
        db.session.add(rating)
    else:
        if request.form.get('Delete'):
            db.session.delete(rating)
        else:
            rating.content = request.form.get('Content')
            rating.updatedAt = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'Success'})

@app.route('/tagging', methods=['POST'])
@login_required
def tagging():
    tagging = Taggings.query.filter_by(authorId=current_user.get_id(), postId=request.form.get('PostId')).first()
    if tagging is None:
        tagging = Taggings(postId=request.form.get('PostId'), authorId=current_user.get_id())
        db.session.add(tagging)
    else:
        if request.form.get('Delete'):
            db.session.delete(tagging)
    db.session.commit()
    return jsonify({'status': 'Success'})

