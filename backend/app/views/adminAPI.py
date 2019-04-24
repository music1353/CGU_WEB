from app import app
from config import MONGO_URI, BASE_DIR, client
from flask import jsonify, session, request
from datetime import datetime
import pprint

# 連進MongoDB
db = client['cgu_db']

# 設置密鑰
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/api/admin/getUsers', methods=['GET'])
def admin_get_users():
    '''取得所有使用者的資料
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': account, name, authority, phone
            'msg': ''
        }
    '''

    user_collect = db['users']
    user_doc = user_collect.find({}, {'_id': False})

    parent_collect = db['parents']
    parent_doc = parent_collect.find({}, {'_id': False})

    users_data = []
    for user in list(user_doc):
        obj = {
            'account': user['account'],
            'name': user['name'],
            'authority': user['authority'],
            'phone': user['phone']
        }
        users_data.append(obj)

    for parent in list(parent_doc):
        obj = {
            'account': parent['account'],
            'name': parent['name'],
            'authority': parent['authority'],
            'phone': parent['phone']
        }
        users_data.append(obj)

    resp = {
        'status': '200',
        'result': users_data,
        'msg': '取得所有使用者資料成功'
    }
    return jsonify(resp)


@app.route('/api/admin/getDailyUsersInfo', methods=['GET'])
def admin_get_daily_users_info():
    '''取得每日所有users的資料以及有無完成每日遊戲
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{account, name, authority, complete}]
            'msg': ''
        }
    '''

    user_collect = db['users']
    user_doc = user_collect.find({}, {'_id': False})
    user_doc_list = list(user_doc)

    daily_collect = db['users_daily_games']
   
    resp_list = []
    for user in user_doc_list:
        obj = {
            'account': '',
            'name': '',
            'authority': '',
            'complete': False
        }
        if 'user' in user['authority']:
            obj['account'] = user['account']
            obj['name'] = user['name']
            obj['authority'] = user['authority']
            daily_doc = daily_collect.find({'account': user['account']}, {'_id': False})
            obj['complete'] = list(daily_doc)[0]['complete']
            resp_list.append(obj)

    resp = {
        'status': '200',
        'result': resp_list,
        'msg': '取得每日使用者資料及complete成功'
    }
    return jsonify(resp)


@app.route('/api/admin/getFeedback', methods=['GET'])
def admin_get_feedback():
    '''取得請求日期的家長的回饋
    Params:
        date
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{pAccount, pName, pAuthority, chAccount, chName, focusValue, emotionValue, motivationValue, feedback}]
            'msg': ''
        }
    '''

    date = request.args.get('date')
    print(date)

    user_collect = db['users']
    doc = user_collect.aggregate([
        {
            '$lookup': {
                'from': "parents",
                'localField': "account",
                'foreignField': "childrenAccount",
                'as': "feedback_doc"
                
            }
        }
    ])
    doc_list = list(doc)

    result_list = []
    for item in doc_list:
        chName = item['name']
        chAccount = item['account']

        feedback_doc = list(item['feedback_doc']).pop()
        pName = feedback_doc['name']
        pAccount = feedback_doc['account']
        pAuthority = feedback_doc['authority']

        focusValue = ''
        emotionValue = ''
        motivationValue = ''
        feedback = ''
        
        for content in feedback_doc['questionnaires']:
            if content['date'] == date:
                focusValue = content['focusValue']
                emotionValue = content['emotionValue']
                motivationValue = content['emotionValue']
                feedback = content['feedback']
        
                obj = {
                    'chName': chName,
                    'chAccount': chAccount,
                    'pName': pName,
                    'pAccount': pAccount,
                    'pAuthority': pAuthority,
                    'focusValue': focusValue,
                    'emotionValue': emotionValue,
                    'motivationValue': motivationValue,
                    'feedback': feedback
                }
                result_list.append(obj)
            

    resp = {
        'status': '200',
        'result': result_list,
        'msg': '取得家長回饋成功'
    }
    return jsonify(resp)



