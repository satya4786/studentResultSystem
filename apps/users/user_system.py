import traceback
import uuid
import hmac
import base64
import hashlib
from apps.models import User
from configs.config import config_dict
from passlib.context import CryptContext
from schema import Schema, SchemaError, And, Use

__AUTHOR__ = "RAMESH KUMAR"


class UserSystem():
    def __init__(self):
        self.secret = "future-track-vision"
        self.algorithm = 'HS256'
        self._pwd_context = None

    @property
    def pwd_context(self):
        if not self._pwd_context:
            self._pwd_context = CryptContext(
                schemes=["pbkdf2_sha256", "des_crypt"],
                default="pbkdf2_sha256",
                all__vary_rounds=0.1,
                pbkdf2_sha256__default_rounds=8000
            )
        return self._pwd_context

    def generate_api_token(self, hash_text):
        data = str(uuid.uuid4()) + hash_text
        dig = hmac.new(self.secret, msg=data, digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def check_user_existence(self, email, phone):
        query = {"$or": [{"email": email}, {"phone": phone}]}
        user_check = User.objects(__raw__=query).first()
        if user_check:
            return True, "User exists in the system"
        else:
            return False, "User not exists"

    def validate_signup_payload(self, data):
        req_keys = eval(config_dict['user']['req_keys'])
        difference = list(set(req_keys).difference(data))
        if difference:
            return False, "Missing expected fields %s" % difference
        return True, "Valid Input"

    def create_user(self, data, is_active=True):
        valid_input, valid_input_message = self.validate_signup_payload(data)
        if not valid_input:
            return {"success": valid_input, "message": valid_input_message}
        is_exists, exists_message = self.check_user_existence(data["email"], data["phone"])
        if is_exists:
            return {"success": True, "message": exists_message}

        try:
            hash_text = data["email"] + data["phone"] + data["full_name"]
            hash_object = hashlib.md5(hash_text)
            unique_hash = hash_object.hexdigest()
            try:
                validation = Schema({
                    'full_name': And(basestring, lambda n: 30 >= len(n) >= 3,
                                     error="Minimum 3 Characters are Required"),
                    'email': And(basestring, lambda n: len(n) >= 3, error="Minimum 3 Characters are Required"),
                    'phone': And(basestring, lambda n: len(n) >= 6, error="Minimum 6 Characters are Required"),
                    "password": And(basestring, lambda n: len(n) >= 6, error="Minimum 6 Characters are Required")
                }).validate(data)
            except SchemaError as e:
                error = e.message
                return {"success": False, "message": error}

            account_create = User()
            user_id = str(uuid.uuid4())
            account_create.username = user_id
            account_create.email = data['email']
            account_create.phone = data['phone']
            account_create.full_name = data['full_name']
            account_create.is_active = is_active
            account_create.password = self.pwd_context.encrypt(data['password'])
            account_create.token = self.generate_api_token(unique_hash)
            account_create.save()

            return {"success": True, "message": "Created User Successfully"}

        except Exception as e:
            print traceback.format_exc()
