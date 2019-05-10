from app import app
from config import MONGO_URI, client
from flask import jsonify, session, request
from datetime import datetime

# 連進MongoDB
db = client['cgu_db']

# 設置密鑰
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/api/data/user', methods=['GET'])
def get_data_user():
    '''取得使用者資料
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{authority, name, account, pwd, token, parentName, parentAccount, parentPwd, phone}]
            'msg': ''
        }
    '''

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
        obj = {
            'authority': '',
            'name': '',
            'account': '',
            'pwd': '',
            'token': '',
            'parentName': '',
            'parentAccount': '',
            'parentPwd': '',
            'phone': ''
        }

        if 'Test' in item['authority']:
            obj['authority'] = '實驗組'
        else:
            obj['authority'] = '對照組'
        
        obj['name'] = item['name']
        obj['account'] = item['account']
        obj['pwd'] = item['pwd']
        obj['token'] = item['token']
        
        feedback_doc = list(item['feedback_doc']).pop()
        obj['parentName'] = feedback_doc['name']
        obj['parentAccount'] = feedback_doc['account']
        obj['parentPwd'] = feedback_doc['pwd']
        obj['phone'] = feedback_doc['phone']

        result_list.append(obj)

    resp = {
        'status': '200',
        'result': result_list,
        'msg': '取得使用者資料成功'
    }
    return jsonify(resp)


@app.route('/api/data/parent', methods=['GET'])
def get_data_parent():
    '''取得家長資料
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{authority, account, pwd, name, phone}]
            'msg': ''
        }
    '''

    collect = db['parents']
    doc = collect.find({}, {'_id': False})
    doc_list = list(doc)

    result_list = []
    for item in doc_list:
        obj = {
            'authority': '',
            'account': '',
            'pwd': '',
            'name': '',
            'phone': ''
        }

        if 'Test' in item['authority']:
            obj['authority'] = '實驗組'
        else:
            obj['authority'] = '對照組'

        obj['name'] = item['name']
        obj['account'] = item['account']
        obj['pwd'] = item['pwd']
        obj['phone'] = item['phone']
        result_list.append(obj)

    resp = {
        'status': '200',
        'result': result_list,
        'msg': '取得家長資料成功'
    }
    return jsonify(resp)


@app.route('/api/data/admin', methods=['GET'])
def get_data_admin():
    '''取得管理員資料
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{authority, account, pwd, name}]
            'msg': ''
        }
    '''

    collect = db['admins']
    doc = collect.find({}, {'_id': False})
    doc_list = list(doc)

    result_list = []
    for item in doc_list:
        obj = {
            'authority': '',
            'account': '',
            'pwd': '',
            'name': ''
        }

        obj['authority'] = item['authority']
        obj['name'] = item['name']
        obj['account'] = item['account']
        obj['pwd'] = item['pwd']
        result_list.append(obj)

    resp = {
        'status': '200',
        'result': result_list,
        'msg': '取得管理員資料成功'
    }
    return jsonify(resp)


@app.route('/api/data/game', methods=['GET'])
def get_data_game():
    '''取得遊戲紀錄資料
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{ account, records: [{date, gameNameEN, level, respTime, trueRate}] }]
            'msg': ''
        }
    '''

    collect = db['users_games_records']
    doc = collect.find({}, {'_id': False})
    doc_list = list(doc)

    resp = {
        'status': '200',
        'result': doc_list,
        'msg': '取得遊戲紀錄資料成功'
    }
    return jsonify(resp)


@app.route('/api/data/questionnaires', methods=['GET'])
def get_data_questionnaires():
    '''取得問卷資料
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{ authority, account, name, parentAccount, parentName, questionnaires:[{date, focusValue, emotionValue, motivationValue, feedback}] }]
            'msg': ''
        }
    '''

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
        obj = {
            'authority': '',
            'name': '',
            'account': '',
            'parentName': '',
            'parentAccount': '',
            'questionnaires': []
        }

        if 'Test' in item['authority']:
            obj['authority'] = '實驗組'
        else:
            obj['authority'] = '對照組'
        
        obj['name'] = item['name']
        obj['account'] = item['account']
        
        feedback_doc = list(item['feedback_doc']).pop()
        obj['parentName'] = feedback_doc['name']
        obj['parentAccount'] = feedback_doc['account']
        
        for content in feedback_doc['questionnaires']:
            obj['questionnaires'].append(content)
        result_list.append(obj)

    resp = {
        'status': '200',
        'result': result_list,
        'msg': '取得問卷資料成功'
    }
    return jsonify(resp)