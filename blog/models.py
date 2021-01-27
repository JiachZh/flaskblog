from datetime import datetime
from blog import db

class Posts(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.categoryId'), nullable = False, )
    url = db.Column(db.String(40), nullable = False, unique=True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    image = db.Column(db.String(80), nullable=False, default='/static/img/defaultPostImage.jpg')
    createdAt = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Integer, nullable=False)
    listed = db.Column(db.Integer, nullable=False)
    pinned = db.Column(db.Integer, nullable=False)

class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(40), nullable=False)
    lastName = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    passwordHash = db.Column(db.String(40), nullable=False)
    comment = db.relationship('Comments', backref = 'user', lazy=True)
    ratings = db.relationship('Ratings', backref='user', lazy = True)

class Categories(db.Model):
    categoryId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

class Comments(db.Model):
    CommentId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('posts.postId'), nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Integer, nullable=False)

class Ratings(db.Model):
    RatingId = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('posts.postId'), nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Integer, nullable=False)
