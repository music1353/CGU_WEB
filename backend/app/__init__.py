from flask import Flask
from flask_cors import *

app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app, resources=r'/*')

from app.views import baseAPI, userAPI, adminAPI, parentAPI, tokenAPI, dataAPI, giftAPI, rankAPI
