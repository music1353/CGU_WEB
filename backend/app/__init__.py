from flask import Flask
import logging
import coloredlogs

app = Flask(__name__)
app.config.from_object('config.Config')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
coloredlogs.install(level='DEBUG')

from app.views import baseAPI, userAPI, adminAPI, parentAPI, tokenAPI, dataAPI, giftAPI, rankAPI
