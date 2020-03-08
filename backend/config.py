import os
# import pymongo
from pymongo import MongoClient

BASE_DIR = os.getcwd()
MODULE_DIR = os.path.join(os.getcwd(), 'app/modules/')
# MONGO_URI= 'mongodb://localhost:27017'
MONGO_URI= 'mongodb://cguot.tk:27017'

try:
    client = MongoClient(MONGO_URI)
    # client = MongoClient(host='db', port=27017)
    print('成功連接至mongodb')
except:
    print('連接mongodb失敗')

class Config(object):
    JSON_AS_ASCII = False
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'