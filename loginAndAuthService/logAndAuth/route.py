from flask import render_template, url_for, flash, redirect, request, Response, session,jsonify
from flask_login import login_user, current_user, logout_user, login_required

from logAndAuth import app, db, bcrypt
from logAndAuth.forms.forms import Validations
from logAndAuth.model.models import User
from logAndAuth.exceptions import UserNameValidationError,EmailDoesNotExist,EmailAndPasswordDoNotMatch,EmailValidationError

import uuid
import datetime

response_template = {
    'session_id':None,
    'response_code':200,
    'error_code':None
    }

session_template = {
    'username':None,
    'accessPermission':None,
    'emailId':None,
    'lastUpdatedSession':None,
    'lastServiceUsed':None
    }

SERVICE_NAME = 'loginAndAuthService'
validationObj = Validations()


@app.route("/register", methods=['GET', 'POST'])
def register():
    response = response_template.copy()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    try:
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



@app.route("/login", methods=['GET', 'POST'])
def login():
    response = response_template.copy()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")

    try:
        validationObj.validate_email_password(email,password)
        user = User.query.filter_by(email=email).first()
        login_user(user, remember=remember)


        session_id = str(uuid.uuid4())
        session_data = session_template.copy()
        session_data['username'] = user.username
        session_data['emailId'] = email
        session_data['accessPermission'] = user.isadmin
        session_data['lastUpdatedSession'] = datetime.datetime.now()
        session_data['lastServiceUsed'] = SERVICE_NAME
        session[session_id] = session_data

        response['response_code'] = 200
        response['session_id'] = session_id

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    except EmailAndPasswordDoNotMatch:
        response['response_code'] = 406
        response['error_code'] = 14

    print (response)
    return response



@app.route("/getAuthorized/<string:session_id>", methods=['GET', 'POST'])
def getAuthorized(session_id):
    response = response_template.copy()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    try:
        session_data = session['session_id']
        email = session_data['email']
        user = User.query.filter_by(email=email).first()
        Validations.validate_email(email)
        session.pop(session_id)

        session_id = uuid.uuid4()
        session_data['lastUpdatedSession'] = datetime.datetime.now()
        session[session_id] = session_data

        response['response_code'] = 200
        response['session_id'] = str(session_id)

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    print (response)
    return response


@app.route("/logout/<string:session_id>")
def logout(session_id):
    logout_user()
    session_data = session[session_id]
    email = session_data['email']
    response = response_template.copy()
    try:
        user = User.query.filter_by(email=email).first()
        Validations.validate_email(email)
        session.pop(session_id)

        response['response_code'] = 200

    except EmailDoesNotExist:
        response['response_code'] = 406
        response['error_code'] = 13
    return response