from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
import os

__author__ = 'Ramesh Kumar'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

store = RedisStore(redis.StrictRedis())
app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'
app.config['CELERY_ENABLE_UTC'] = True
app.config['SECRET_KEY'] = 'trackvision473'
KVSessionExtension(store, app)
