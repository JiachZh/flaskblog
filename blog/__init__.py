from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__, static_folder='static') 
app.config['SECRET_KEY'] = 'AAABBBCCDDDEE'


# app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://c2098620:MYSQL_8023Cake,.@csmysql.cs.cf.ac.uk:3306/c2098620_flaskBlog'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mysun:3.1415926@138.197.179.225:3306/flaskblog'

db = SQLAlchemy(app)