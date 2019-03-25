import json
from apps import app
from apps.users.user_system import UserSystem
from flask import jsonify, request

__AUTHOR__ = "RAMESH KUMAR"


@app.route('/')
@app.route('/_health')
def health_check_api():
    return "Welcome to Track Vision Application"


@app.route("/signup", methods=['POST'])
def signup_api():
    """
        by Ramesh Kumar
        -------
        :param text: email, phone, full_name, password
        :return: signup response in JSON Format

    """
    input_data = json.loads(request.data)
    usersystem = UserSystem()
    response = usersystem.create_user(input_data)
    return jsonify(response)

@app.route("/login", methods=['POST'])
def login_api():
    """
    By satya Kumari
    -------
    :param text email,phone,password
    :return :text login sucessfull or invalid login
    """
    input_data =json.loads(request.data)
    username=input_data['username']
    password=input_data['password']
    if username and password :
        usersystem=UserSystem()
        response=usersystem.verify_loggedin_user(username,password)
        return jsonify(response)
    else:
        return jsonify({'message': 'Please enter valid username and password'})
