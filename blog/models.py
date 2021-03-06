import datetime
from blog import db
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    username = db.StringField(max_length=255, unique=True)#, primary_key=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    meta = {
        'indexes': ['-confirmed_at', 'email', 'username']
    }

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    content = db.StringField()
    name = db.StringField(max_length=120)
    email = db.StringField(max_length=120)

class Tag(db.Document):
    name = db.StringField(max_length=50, unique=True)

class DefaultContent(db.EmbeddedDocument):
    content = db.StringField(default='')

class TodoElement(db.EmbeddedDocument):
    content = db.StringField(default='')
    key = db.IntField()
    done = db.BooleanField(default=False)
    status = db.StringField(max_length=50, default='todo')

class TodoContent(db.EmbeddedDocument):
    elements = db.ListField(db.EmbeddedDocumentField('TodoElement'))

class ReviewContent(db.EmbeddedDocument):
    title = db.StringField()
    year = db.IntField()
    authors = db.ListField(db.StringField)
    journal = db.StringField()
    content = db.StringField()

class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=120, default='')
    owner = db.ReferenceField(User, required=True)
    read = db.ListField(db.ReferenceField(User), default=[])
    write = db.ListField(db.ReferenceField(User), default=[])
    content = db.GenericEmbeddedDocumentField()
    category = db.StringField(default='default')
    tags = db.ListField(db.ReferenceField('Tag'), default=[])
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    # Status: 'public' or 'private'
    status = db.StringField(max_length=120, default='private')

    meta = {
        'indexes': ['-created_at', 'tags', 'category', 'name',
                    'status', 'owner', 'read', 'write'],
        'ordering': ['-created_at', 'tags'],
    }

    @classmethod
    def list(cls, user, *args, **kwargs):
        posts = cls.objects.all(*args, **kwargs)
        res = [post for post in posts if post.can_read(user)]
        return res

    @db.queryset_manager
    def public(doc_cls, queryset):
        return queryset.filter(status='public')

    def can_edit(self, user):
        if user == self.owner:
            return True
        elif user in self.write:
            return True
        return False
    
    def can_read(self, user):
        if user == self.owner:
            return True
        elif user in self.write:
            return True
        elif user in self.read:
            return True
        return False

            
    def save(self, user, *args, **kwargs):
        if self.owner == user:
            super(Post, self).save(*args, **kwargs)


