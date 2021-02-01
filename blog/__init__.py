from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_folder='static') 
app.config['SECRET_KEY'] = 'AAABBBCCDDDEE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://c2098620:8023Cake8023@csmysql.cs.cf.ac.uk:3306/c2098620_flaskblog'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysun:3.1415926@138.197.179.225:3306/flaskblog'

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from blog import routes
