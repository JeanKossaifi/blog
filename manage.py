# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask.ext.script import Manager, Server
from flask.ext.security import Security, MongoEngineUserDatastore
from flask_bootstrap import Bootstrap
import json

from blog.models import *
from blog import app

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
Bootstrap(app)
security = Security(app, user_datastore)
manager = Manager(app)

@manager.command
def drop():
    Tag.drop_collection()
    Post.drop_collection()
    User.drop_collection()
    print('Database dropped.')

@manager.command
def init():
    drop()
    tag = Tag(name='test')
    tag.save()
    tag2 = Tag(name='tag')
    tag2.save()
    content = DefaultContent(content='hello!!\n new article')
    user_datastore.create_user(email='test', password='test', username='test')
    user_datastore.create_user(email='user', password='user', username='user')
    user_datastore.create_user(email='jean', password='jean', username='jean')
    jean = User.objects.get(username='jean')
    test = User.objects.get(username='test')
    post = Post(name='name article',
                owner=jean,        
                content=content,
                category='default',
                tags = [tag, tag2],
                status = 'private')
    post.save(user=jean)
    post = Post(name='test article',
                owner=test,        
                content=content,
                category='default',
                tags = [tag, tag2],
                status = 'private')
    post.save(user=test)
    post = Post(name='test article 2',
                owner=test,        
                read=[jean],
                content=content,
                category='default',
                tags = [tag, tag2],
                status = 'public')
    post.save(user=test)




# To save the db in a file:
# mongoexport -d blog -c blog -o '/path/savefile.json'
# To import back:
# mongoimport -d blog -c blog --file '/path/savefile.json'

# Create a user to test with
@app.before_first_request
def create_user():
    pass
    #user_datastore.create_user(email='jean', password='jean', username='jean')

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    port = 55555,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()
