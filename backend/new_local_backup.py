import os
import pymongo
from bson import json_util
from datetime import datetime
import json

MONGO_URI= 'mongodb://34.80.254.96:27017'

client = pymongo.MongoClient(MONGO_URI)

nowTime = datetime.now().strftime("%Y-%m-%d") # 今天日期

# 創建資料夾
try:
    mkdir_cmd = 'mkdir ./backup/' + nowTime # in linux
    # mkdir_cmd = 'mkdir .\\backup\\' + nowTime # in win
    os.system(mkdir_cmd)
    print('創建', nowTime, '資料夾成功！')
except Exception as err:
    print('創建', nowTime, '資料夾失敗！')
    print('err:', err)

# backup all collections
db = client['cgu_db']
collections_name = db.collection_names()

for col_name in collections_name:
    col = db[col_name]
    cursor = col.find({})

    file = open('./backup/'+nowTime+'/'+col_name+'.json', "w", encoding='utf-8')
    for document in cursor:
        file.write(json.dumps(document, default=json_util.default, ensure_ascii=False))
        file.write('\n')
        
    print('complete backup', col_name)

