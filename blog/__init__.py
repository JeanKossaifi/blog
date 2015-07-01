from flask import Flask
from flask.ext.mongoengine import MongoEngine

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'My_bl0g_keY'

# MongoDB Config
app.config['MONGODB_DB'] = 'blog'
app.config['MONGODB_HOST'] = 'localhost'
#app.config['MONGODB_PORT'] = 27017

db = MongoEngine(app)

def add_views():
    # Avoid cyclic include
    from blog import views

def add_api():
    from blog import api

add_views()
add_api()
