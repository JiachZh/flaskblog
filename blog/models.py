from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from blog import db, login_manager

class Posts(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.categoryId'), nullable = False, )
    url = db.Column(db.String(40), nullable = False, unique=True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    image = db.Column(db.String(80), nullable=False, default='/static/img/defaultPostImage.jpg')
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Integer, nullable=False, default=0)
    listed = db.Column(db.Integer, nullable=False, default=0)
    pinned = db.Column(db.Integer, nullable=False, default=0)
    comments = db.relationship('Comments', backref='post', lazy=True)
    ratings = db.relationship('Ratings', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.createdAt}', '{self.url}', '{self.title}')"

class Users(UserMixin, db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(40), nullable=False)
    lastName = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    userName = db.Column(db.String(40), nullable=False, unique=True)
    passwordHash = db.Column(db.String(128), nullable=False)
    comment = db.relationship('Comments', backref='user', lazy=True)
    ratings = db.relationship('Ratings', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return self.userId

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

class Categories(db.Model):
    categoryId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    post = db.relationship('Posts', backref='post', lazy=True)

class Comments(db.Model):
    commentId = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('posts.postId'), nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Comment('{self.createdAt}', '{self.authorId}', '{self.content}')"

class Ratings(db.Model):
    ratingId = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Integer, nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('posts.postId'), nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Rating('{self.createdAt}', '{self.authorId}', '{self.content}')"
