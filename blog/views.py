from blog.models import *
from blog import app, db
from flask import request, jsonify, render_template, redirect, url_for, session
import json
import markdown
from docutils.core import publish_parts
from flask.ext.security import logout_user, current_user

@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/blog')
def blog():
    posts = Post.objects(status='public')
    return render_template('post_list.html', 
                           posts=posts)

@app.route('/debug')
def debug():
    crash


@app.route('/tag/new', methods=['GET', 'POST'])
@login_required
def new_tag():
    if request.method == 'POST':
        tag_name = request.form['tagname']
        new_tag = Tag(name=tag_name)
        new_tag.save()
        return '''Hello, you have added something ;)
                <a href='/post/list'>
                back to the list
                </a>
                '''
    tags = [tag['name'] for tag in Tag.objects.all()]
    return render_template('new_tag.html', tags=tags)
           

@app.route('/post/list')
@login_required
def post_list():
    posts = Post.get_list(current_user)
    return render_template('post_list.html', 
                           posts=posts)


def parse_content(category, form):
    """Parses the form for a given category of post and returns the content.
    """
    if category == 'default':
        content = DefaultContent()
        content.content = form['default_content']

    elif category == 'todo':
        content = TodoContent()
        n_elements = int(form.get('n_elements'))
        for value in range(n_elements):
            key = str(value)
            element = TodoElement(content=form.get(key),
                                  key=value)
            content.elements.append(element)

    elif category == 'review':
        content = ReviewContent()
        content.content = form['review_content']
        content.journal = form['journal']
        content.title = form['title']

    return content

@app.route('/post/new/<string:category>', methods=['GET'])
@login_required
def new_post(category):
    """Returns a new content for the given category
    """

    if category == 'default':
        content = DefaultContent(content='')

    elif category == 'todo':
        content = TodoContent()

    elif category == 'review':
        content = ReviewContent()

    post = Post(content=content)
    return render_template('edit_post.html',
                           category=category,
                           post=post)


@app.route('/post/view/<string:category>/<string:pk>', methods=['GET'])
@login_required
def view_post(category, pk):
    """Returns a new content for the given category
    """
    post = Post.objects.get(pk=pk)
    return render_template('view_post.html',
                           category=category,
                           post=post)



@app.route('/post/edit/<string:category>/<string:pk>', methods=['GET', 'POST'])
@app.route('/post/edit/<string:category>', methods=['POST'])
@login_required
def edit_post(category, pk=None):
    if request.method == 'POST':
        name = request.form['name']
        tags = request.form.getlist('tags')
        if request.form.get('public'):
            status = 'public'
        else:
            status = 'private'
        tags = [Tag.objects.get(name=tag) for tag in tags]

        content = parse_content(category, request.form)

        if pk is None:
            post = Post()
        else:
            post = Post.objects.get(pk=pk)
        post.name = name
        post.category = category
        post.tags = tags
        post.content = content
        post.status = status
        post.save()

        return redirect(url_for('view_post', category=category, pk=post.pk))
    
    elif request.method == 'GET':
        if pk is not None:
            post = Post.objects.get(pk=pk)
            return render_template('edit_post.html',
                                category=category,
                                post=post)
        else: # Shouldn't happen..
            return redirect(url_for('new_post', category=category))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.context_processor
def custom_jinja_fun():

    def date_now(format="%d.m.%Y %H:%M:%S"):
        """ returns the formated datetime """
        return datetime.datetime.now().strftime(format)

    def rst(rst_text):
        """ Return html version of the rst_text """
        return publish_parts(rst_text, writer_name='html')['html_body']

    return dict(date_now=date_now, rst=rst)
