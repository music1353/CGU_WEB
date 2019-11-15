from app import app
from config import client
from flask import jsonify, session, request
from datetime import datetime

# 連進MongoDB
db = client['cgu_db']

@app.route('/api/rank/getRank', methods=['GET'])
def get_rank():
    '''取得排名
    Params:
        authority
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{ranking, account, tokenNum}]
            'msg': ''
        }
    '''

    auth = request.args.get("authority")

    user_collect = db['users']
    user_doc = user_collect.find({}, {'_id': False})
    user_doc_list = list(user_doc)

    # 把需要的資料及符合auth的放入user_data
    user_data = []
    for item in user_doc_list:
      if item['authority'] == auth:
        obj = {
          'account': item['account'],
          'name': item['name'],
          'token': item['token']
        }
        user_data.append(obj)

    # 計算排名
    user_data.sort(key=lambda k: k['token'], reverse=True)
    if len(user_data)>10:
      resp = {
        'status': '200',
        'result': user_data[0:10],
        'msg': '取得金幣排名成功！'
      }
      return jsonify(resp)
    else:
      resp = {
          'status': '200',
          'result': user_data,
          'msg': '取得金幣排名成功！'
      }
      return jsonify(resp)
    

@app.route('/api/rank/getWeek', methods=['GET'])
def get_week():
    '''取得週次
    Params:
        authority
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': week
            'msg': ''
        }
    '''

    week_collect = db['week_count']
    week_doc = week_collect.find_one({'_id': 0})

    re_week = ''
    if  week_doc['week'] == 1:
      re_week = '第一週'
    elif  week_doc['week'] == 2:
      re_week = '第二週'
    elif  week_doc['week'] == 3:
      re_week = '第三週'
    elif  week_doc['week'] == 4:
      re_week = '第四週'
    elif  week_doc['week'] == 5:
      re_week = '第五週'
    elif  week_doc['week'] == 6:
      re_week = '第六週'
    elif  week_doc['week'] == 7:
      re_week = '第七週'
    elif  week_doc['week'] == 8:
      re_week = '第八週'
    elif  week_doc['week'] == 9:
      re_week = '第九週'
    elif  week_doc['week'] == 10:
      re_week = '第十週'
    
    resp = {
      'status': '200',
      'result': {
        'week': re_week
      },
      'msg': '取得週次成功！'
    }
    return jsonify(resp)