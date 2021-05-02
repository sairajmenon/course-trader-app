from flask import  request,abort

from courseAndDiscussion import app, db
from courseAndDiscussion.model.models import Post,User
from courseAndDiscussion.exceptions import InvalidSessionID

import datetime
from bson import json_util
import json
import os
import redis

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

response_template = {
    'session_id':None,
    'response_code':200,
    'error_code':None,
    'results':None,
    }

discussions = {
    'discussion_id':None,
    'is_editable':False,
    'username':None,
    'title':None,
    'content':None,
    'date_posted':None
}


session_template = {
    'username':None,
    'accessPermission':None,
    'emailId':None,
    'lastUpdatedSession':None,
    'lastServiceUsed':None
    }

# formString = """
#     <div>
#         <form method='POST' action=''>
#             <fieldset class='form-group'>
#                 <legend class='border-bottom mb-4'>Title</legend>
#                 <div class='form-group'>
#                    <input type='text' id='title' name='title' value='{0}'><br>
#                 </div>
#                 <div class='form-group'>
#                     <legend class='border-bottom mb-4'>Content</legend>
#                   <input type='text' id='content' name='content' value='{1}'><br>
#                 </div>
#                 <div class='form-group'>
#                     <button type='submit' class='btn btn-primary'>Submit</button>
#                 </div>
#             </fieldset>
#         </form>
#     </div>
# """

SERVICE_NAME = 'CourseDiscussionService'

@app.route("/discussions/new", methods=['GET', 'POST'])
def new_post():
    response = response_template.copy()
    try:
        title = request.form.get("title")
        content = request.form.get("content")
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exists")
        session_data = json.loads(session_data, object_hook=json_util.object_hook)
        author = session_data['user_id']
        user = User.query.filter_by(id=author).first_or_404()
        post = Post(title=title, content=content, author=user)
        db.session.add(post)
        db.session.commit()
        response['session_id'] = session_id
        return response
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14

def populateDiscussion(post,username):
    discussion = discussions.copy()
    discussion['discussion_id'] = post.id
    discussion['is_editable'] = True if post.username==username else False
    discussion['username'] = post.username
    discussion['title'] = post.title
    discussion['content'] = post.content
    discussion['date_posted'] = post.date_posted
    return discussion

def get_paginated_list(page,username):
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    data = {}
    data['page'] = posts.page
    data['total'] = posts.pages
    discussions = []
    counter = 0
    for post in posts.items:
        counter += 1
        discussion_data = populateDiscussion(post,username)
        discussions.append(discussion_data)
    data['discussions'] = discussions
    return data


@app.route("/discussions")
def post():
    response = response_template.copy()
    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        session_data = json.loads(session_data, object_hook=json_util.object_hook)
        username = session_data['username']
        if not session_data:
            raise InvalidSessionID("Session does not exists")
        page = request.args.get('page', 1, type=int)
        response['results'] = get_paginated_list(page,username)
        response['session_id'] = session_id
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    return response


@app.route("/discussions/<int:discussion_id>")
def getpost(discussion_id):
    response = response_template.copy()
    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        session_data = json.loads(session_data, object_hook=json_util.object_hook)
        username = session_data['username']

        if not session_data:
            raise InvalidSessionID("Session does not exists")
        post = Post.query.get_or_404(discussion_id)
        response['results'] = {'data':populateDiscussion(post,username)}
        response['session_id'] = session_id

    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    return response


@app.route("/discussions/<int:discussion_id>/update", methods=['POST'])
def update_post(discussion_id):
    post = Post.query.get_or_404(discussion_id)
    response = response_template.copy()
    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exits")

        session_data = json.loads(session_data, object_hook=json_util.object_hook)
        user_id = session_data['user_id']
        current_user = User.query.filter_by(id=user_id).first_or_404()

        if post.author != current_user:
            abort(403)

        if request.method == "POST":
            title = request.form.get("title")
            content = request.form.get("content")

            post.title = title
            post.content = content
            post.date_posted = datetime.datetime.now()
            db.session.commit()

            return getpost(discussion_id)


    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14

    return response


@app.route("/discussions/<int:discussion_id>/delete", methods=['POST','DELETE'])
def delete_post(discussion_id):
    response = response_template.copy()
    try:
        post = Post.query.get_or_404(discussion_id)
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exists")

        session_data = json.loads(session_data, object_hook=json_util.object_hook)
        user_id = session_data['user_id']
        current_user = User.query.filter_by(id=user_id).first_or_404()

        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        response['session_id'] = session_id
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    return response

def get_paginated_list_for_user(page,user):
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)

    data = {}
    data['page'] = posts.page
    data['total'] = posts.pages
    discussions = []
    counter = 0
    for post in posts.items:
        counter += 1
        discussion_data = populateDiscussion(post,user.username)
        discussions.append(discussion_data)
    data['discussions'] = discussions
    return data


@app.route("/discussions/user/<string:username>")
def user_posts(username):
    response = response_template.copy()
    try:
        session_id = request.headers.get('session_id')
        if not session_id:
            raise InvalidSessionID("Session not available")
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=username).first_or_404()
        response['results'] = get_paginated_list_for_user(page,user)
        response['session_id'] = session_id
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    return response

