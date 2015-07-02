from blog.models import *
from blog import app, db
from flask import request, jsonify, render_template
import json
import markdown


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/blog')
def blog():
    posts = Post.objects(status='public')
    return render_template('list_posts.html', 
                           posts=posts)


@app.route('/posts')
@login_required
def list_posts():
    posts = Post.objects.all()
    return render_template('list_posts.html', 
                           posts=posts)


@app.route('/add/tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    if request.method == 'POST':
        tag_name = request.form['tagname']
        new_tag = Tag(name=tag_name)
        new_tag.save()
        return '''Hello, you have added something ;)
                <a href='/posts'>
                back to the list
                </a>
                '''
    tags = [tag['name'] for tag in Tag.objects.all()]
    return render_template('add_tag.html', tags=tags)
           

@app.route('/post/default/<string:pk>', methods=['GET', 'POST'])
@app.route('/post/default', methods=['GET', 'POST'])
@login_required
def add_default_post(pk=None):
    if request.method == 'POST':
        name = request.form['name']
        tags = request.form['tags']
        if request.form.get('public'):
            status = 'public'
        else:
            status = 'private'
        content = DefaultContent()
        content.text = request.form['default_content']

        # TODO: replace tags with a list of tags
        # Currently only one tag name
        tag = Tag.objects.get(name=tags)
        category = 'default'
        if pk is None:
            post = Post(name=name,
                        category=category,
                        tags = [tag],
                        content=content,
                        status=status)
        else:
            post = Post.objects.get(pk=pk)
            post.name = name
            post.category = category
            post.tags = [tag]
            post.content = content
            post.status = status
        post.save()
        return 'done'
    
    elif request.method == 'GET':
        if pk is not None:
            post = Post.objects.get(pk=pk)
        else:
            post = Post(content=DefaultContent())
        return render_template('default_post.html',
                                post=post)


@app.route('/post/todo/<string:pk>', methods=['GET', 'POST'])
@app.route('/post/todo', methods=['GET', 'POST'])
@login_required
def add_todo_post(pk=None):
    if request.method == 'POST':
        name = request.form['name']
        tags = request.form['tags']
        if request.form.get('public'):
            status = 'public'
        else:
            status = 'private'
        content = TodoContent()
        print(request.form)
        n_elements = int(request.form.get('n_elements'))
        for value in range(n_elements):
            key = str(value)
            element = TodoElement(content=request.form.get(key),
                                  key=value)
            content.elements.append(element)

        # TODO: replace tags with a list of tags
        # Currently only one tag name
        tag = Tag.objects.get(name=tags)
        category = 'todo'
        if pk is None:
            post = Post(name=name,
                        category=category,
                        tags = [tag],
                        content=content,
                        status=status)
        else:
            post = Post.objects.get(pk=pk)
            post.name = name
            post.category = category
            post.tags = [tag]
            post.content = content
            post.status = status
        post.save()
        return 'done'
    
    elif request.method == 'GET':
        if pk is not None:
            post = Post.objects.get(pk=pk)
        else:
            post = Post()
            content = TodoContent()
        return render_template('todo_post.html',
                                post=post)
