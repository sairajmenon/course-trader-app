from flask import request

from logAndAuth import app, db, bcrypt
from logAndAuth.forms.forms import Validations
from logAndAuth.model.models import User
from logAndAuth.exceptions import UserNameValidationError,EmailDoesNotExist,EmailAndPasswordDoNotMatch,EmailValidationError,InvalidSessionID
import os
import redis
import uuid
import datetime
from bson import json_util
import json

redis_host = os.environ.get('REDISHOST', 'localhost')
redis_port = int(os.environ.get('REDISPORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

response_template = {
    'session_id':None,
    'response_code':200,
    'error_code':None,
    'data':None
    }


session_template = {
    'user_id':None,
    'username':None,
    'accessPermission':None,
    'email':None,
    'lastUpdatedSession':None,
    'lastServiceUsed':None
    }

SERVICE_NAME = 'loginAndAuthService'
validationObj = Validations()


@app.route("/logAndAuth/register", methods=['GET', 'POST'])
def register():
    response = response_template.copy()

    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        print ("username and email",username,email)
        validationObj.validate_username_email(username,email)
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, isadmin=False,email=email, password=hash_password)

        db.session.add(user)
        db.session.commit()

        response['response_code'] = 200

    except UserNameValidationError:
        response['response_code'] = 406
        response['error_code'] = 11
    except EmailValidationError:
        response['response_code'] = 406
        response['error_code'] = 12

    print (response)
    return response



@app.route("/logAndAuth/login", methods=['GET', 'POST'])
def login():
    response = response_template.copy()
    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")

    try:
        validationObj.validate_email_password(email,password)
        user = User.query.filter_by(email=email).first()
        # login_user(user, remember=remember)


        session_id = str(uuid.uuid4())
        session_data = session_template.copy()
        session_data['username'] = user.username
        session_data['user_id'] = user.id
        session_data['email'] = email
        session_data['accessPermission'] = user.isadmin
        session_data['lastUpdatedSession'] = datetime.datetime.now()
        session_data['lastServiceUsed'] = SERVICE_NAME
        session_data = json.dumps(session_data,default=json_util.default)
        redis_client.set(session_id,session_data)

        response['response_code'] = 200
        response['session_id'] = session_id

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    except EmailAndPasswordDoNotMatch:
        response['response_code'] = 406
        response['error_code'] = 14

    return response

@app.route("/logAndAuth/getUserDetails", methods=['GET'])
def getUserDetails():
    response = response_template.copy()

    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exists")

        session_data = json.loads(session_data, object_hook=json_util.object_hook)

        email = session_data['email']
        user = User.query.filter_by(email=email).first()
        validationObj.verify_email_exists(email=email)

        session_data['lastUpdatedSession'] = datetime.datetime.now()
        session_data = json.dumps(session_data,default=json_util.default)

        response['response_code'] = 200
        response['session_id'] = session_id
        response['data'] = session_data

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14

    return response



@app.route("/logAndAuth/getAuthenticated", methods=['GET', 'POST'])
def getAuthenticated():
    response = response_template.copy()

    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)

        if not session_data:
            raise InvalidSessionID("Session does not exists")

        session_data = json.loads(session_data,object_hook=json_util.object_hook)

        email = session_data['email']
        user = User.query.filter_by(email=email).first()
        validationObj.verify_email_exists(email=email)

        lastUpdatedSession = session_data['lastUpdatedSession'].replace(tzinfo=None)
        print ("lastupdated session",lastUpdatedSession)
        oldtimestamp = datetime.datetime.now() - datetime.timedelta(minutes=15)
        difference = oldtimestamp - lastUpdatedSession
        print ("old time session",oldtimestamp)

        if difference.total_seconds() > 0:
            getAuthorized()

        session_data['lastUpdatedSession'] = datetime.datetime.now()
        session_data = json.dumps(session_data,default=json_util.default)

        redis_client.set(session_id,session_data)

        response['response_code'] = 200
        response['session_id'] = str(session_id)

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14

    return response


@app.route("/logAndAuth/getAuthorized", methods=['GET', 'POST'])
def getAuthorized():
    response = response_template.copy()

    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)
        if not session_data:
            raise InvalidSessionID("Session does not exists")

        session_data = json.loads(session_data, object_hook=json_util.object_hook)

        email = session_data['email']
        user = User.query.filter_by(email=email).first()
        validationObj.verify_email_exists(email=email)

        redis_client.delete(session_id)
        session_id = str(uuid.uuid4())
        session_data['lastUpdatedSession'] = datetime.datetime.now()
        session_data = json.dumps(session_data,default=json_util.default)

        redis_client.set(session_id,session_data)

        response['response_code'] = 200
        response['session_id'] = str(session_id)

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14

    return response



@app.route("/logAndAuth/logout")
def logout():
    # logout_user()
    response = response_template.copy()
    try:
        session_id = request.headers.get('session_id')
        session_data = redis_client.get(session_id)

        if not session_data:
            raise InvalidSessionID("Session does not exists")
        session_data = json.loads(session_data, object_hook=json_util.object_hook)

        email = session_data['email']

        validationObj.verify_email_exists(email)
        redis_client.delete(session_id)
        response['response_code'] = 200
    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    except InvalidSessionID:
        response['response_code'] = 440
        response['error_code'] = 14
    return response