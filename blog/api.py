from blog.models import *
from blog import app, db
from flask import request, jsonify
import json

@app.route('/tag/<string:tag_name>',
           methods=['POST', 'PUT', 'GET'])
def api_tag(tag_name):
    if request.method == 'POST' or request.method == 'PUT' or request.method == 'GET':
        # Try to save the new tag
        try:
            Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            new_tag = Tag(name=tag_name)
            new_tag.save()
        return jsonify(message='success')
    # There can only be one tag with the given name
    if Tag.objects.find(name=tag_name).limit(1):
        return jsonify(article=Article.objects(tags__contains=tag_name))
    else:
        return 'No existing result'

@app.route('/tags/')
def api_tags():
    tags = [tag.name for tag in Tag.objects.all()]
    return jsonify(tags=tags)
