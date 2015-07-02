import datetime
from blog import db
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    name = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    meta = {
        'indexes': ['-confirmed_at', 'email', 'name']
    }


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    content = db.StringField()
    name = db.StringField(max_length=120)
    email = db.StringField(max_length=120)


class Tag(db.Document):
    name = db.StringField(max_length=50, unique=True)

class DefaultContent(db.EmbeddedDocument):
    text = db.StringField(default='')

class TodoElement(db.EmbeddedDocument):
    content = db.StringField(default='')
    key = db.IntField()
    status = db.StringField(max_length=50, default='todo')

class TodoContent(db.EmbeddedDocument):
    elements = db.ListField(db.EmbeddedDocumentField('TodoElement'))

class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=120, default='')
    #author = db.ReferenceField(User)
    content = db.GenericEmbeddedDocumentField()
    category = db.StringField(default='default')
    tags = db.ListField(db.ReferenceField('Tag'))
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    # Status: 'public' or 'private'
    status = db.StringField(max_length=120, default='private')

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'tags', 'category', 'status'],
        'ordering': ['-created_at', 'tags'],
    }

