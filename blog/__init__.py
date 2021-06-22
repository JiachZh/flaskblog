from flask import Flask
import flask_sqlalchemy
from flask_login import LoginManager

app = Flask(__name__, static_folder='static') 
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://'


login_manager = LoginManager()
login_manager.init_app(app)
db = flask_sqlalchemy.SQLAlchemy(app)

from blog import routes, filters, context_processors
