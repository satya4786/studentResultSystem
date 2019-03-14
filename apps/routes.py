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
    response = UserSystem().create_user(input_data)
    return jsonify(response)
