from flask import Flask
import logging
import coloredlogs

app = Flask(__name__)
app.config.from_object('config.Config')

# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# set logging format
fmt = "%(asctime)s : %(levelname)s : %(message)s"
formatter = logging.Formatter(fmt)

# waitress logger
# waitress_logger = logging.getLogger('waitress')
# waitress_fh = logging.FileHandler('logs/waitress.log')
# waitress_fh.setLevel(logging.DEBUG)
# waitress_fh.setFormatter(formatter)
# waitress_logger.addHandler(waitress_fh)

# apscheduler logger
aps_logger = logging.getLogger('apscheduler')
aps_fh = logging.FileHandler('logs/apscheduler.log')
aps_fh.setLevel(logging.DEBUG)
aps_fh.setFormatter(formatter)
aps_logger.addHandler(aps_fh)

coloredlogs.install(level='DEBUG')

from app.views import baseAPI, userAPI, adminAPI, parentAPI, tokenAPI, dataAPI, giftAPI, rankAPI
