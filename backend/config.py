import os
import pymongo

BASE_DIR = os.getcwd()
MODULE_DIR = os.path.join(os.getcwd(), 'app/modules/')
MONGO_URI= 'mongodb://localhost:27017'

try:
    client = pymongo.MongoClient(MONGO_URI)
    print('成功連接至mongodb')
except:
    print('連接mongodb失敗')

class Config(object):
    JSON_AS_ASCII = False
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'