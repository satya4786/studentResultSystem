import datetime
from mongoengine import *
from pymongo import ReadPreference
from configs.config import config_dict

__AUTHOR__ = "RAMESH KUMAR"

db_name = config_dict["mongo"]["dbname"]
connection_str = config_dict['mongo']["host"]
port = config_dict["mongo"]["port"]
if ":" in connection_str:
    replica_set = config_dict["mongo"]["replicaset"]
    host = "mongodb://" + connection_str
    if replica_set:
        host += "/?replicaSet=" + replica_set
    username = config_dict["mongo"]["username"]
    password = config_dict["mongo"]["password"]
    connect(db_name, host=host, read_preference=ReadPreference.PRIMARY, username=username, password=password)
else:
    connect(db_name, host=connection_str, port=int(port))


class User(DynamicDocument):
    username = StringField(required=True, primary_key=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    full_name = StringField(required=True)
    password = StringField(required=True)
    is_active = BooleanField(default=False)
    token = StringField()
    inserted_at = DateTimeField()
    modified_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.inserted_at:
            self.inserted_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        return super(User, self).save(*args, **kwargs)

    meta = {
        'indexes': ['email', 'phone', 'full_name'],
    }
