from app import app
from config import MONGO_URI, client
from flask import jsonify, session, request
from datetime import datetime
import pprint

# 連進MongoDB
db = client['cgu_db']

# 設置密鑰
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/api/admin/getAllUsers', methods=['GET'])
def admin_get_all_users():
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


@app.route('/api/admin/getUsers', methods=['GET'])
def admin_get_users():
    '''取得所有使用者結合家長的資料
    NOTE: 2019.5.7：把小朋友與家長連結起來
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [name, account, parentName, parentAccount, authority, phone]
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
    for user in doc_list:
        obj = {
            'name': user['name'],
            'account': user['account'],
            'parentName': user['feedback_doc'][0]['name'],
            'parentAccount': user['feedback_doc'][0]['account'],
            'authority': user['authority'],
            'phone': user['feedback_doc'][0]['phone']
        }
        result_list.append(obj)

    resp = {
        'status': '200',
        'result': result_list,
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

    result_list = [] = []
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


@app.route('/api/admin/addOneUser', methods=['POST'])
def admin_add_one_user():
    '''增加一位使用者(user綁parent)
    Params:
        authority, account, pwd, name, Pauthority, Paccount, Ppwd, Pname, phone
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    authority = request.json['authority']
    account = request.json['account']
    pwd = request.json['pwd']
    name = request.json['name']
    Pauthority = request.json['Pauthority']
    Paccount = request.json['Paccount']
    Ppwd = request.json['Ppwd']
    Pname = request.json['Pname']
    phone = request.json['phone']
    resp = {} # 回傳的訊息

    user_collect = db['users']
    users_daily_games_collect = db['users_daily_games']
    users_games_level_collect = db['users_games_level']
    users_games_records_collect = db['users_games_records']
    users_mission_collect = db['users_mission']
    parent_collect = db['parents']

    # 檢查此帳號是否已經存在
    user_doc = user_collect.find_one({'account': account}, {'_id': False})
    parent_doc = parent_collect.find_one({'account': Paccount}, {'_id': False})

    if user_doc != None:
        resp = {
            'status': '404',
            'result': '',
            'msg': '新增帳號失敗，此user帳號已經存在！'
        }
        return jsonify(resp)
    elif parent_doc != None:
        resp = {
            'status': '404',
            'result': '',
            'msg': '新增帳號失敗，此parent帳號已經存在！'
        }
        return jsonify(resp)
    else:
        # 新增user帳號
        user_obj = {
            'account': account,
            'pwd': pwd,
            'name': name,
            'authority': authority,
            'token': '0'
        }
        user_collect.insert_one(user_obj)

        # 新增 users_daily_games
        users_daily_games_obj = {
            'account': account,
            'complete': False,
            'games': []
        }
        users_daily_games_collect.insert_one(users_daily_games_obj)

        # 新增 users_games_level
        users_games_level_obj = {
            'account': account,
            'PrePet': '1',
            'BackPet': '1',
            'PreAnimal': '1',
            'BackAnimal': '1',
            'Teacher': '1',
            'Ball': '1',
            'Where': '1'
        }
        users_games_level_collect.insert_one(users_games_level_obj)

        # 新增 users_games_records
        users_games_records_obj = {
            'account': account,
            'records': []
        }
        users_games_records_collect.insert_one(users_games_records_obj)

        # 新增 users_mission
        users_mission_obj = {
            'account': account,
            'loginMission': False,
            'playMission': []
        }
        users_mission_collect.insert_one(users_mission_obj)

        # 新增parent帳號
        parent_obj = {
            'account': Paccount,
            'pwd': Ppwd,
            'name': Pname,
            'phone': phone,
            'authority': Pauthority,
            'childrenAccount': account,
            'questionnaires': []
        }
        parent_collect.insert_one(parent_obj)

        resp = {
            'status': '200',
            'result': '',
            'msg': '新增帳號成功'
        }
        return jsonify(resp)


@app.route('/api/admin/delOneUser', methods=['POST'])
def admin_del_one_user():
    '''刪除一位使用者(user綁parent)
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    account = request.json['account']
    Paccount = request.json['Paccount']   

    user_collect = db['users']
    users_daily_games_collect = db['users_daily_games']
    users_games_level_collect = db['users_games_level']
    users_games_records_collect = db['users_games_records']
    users_mission_collect = db['users_mission']
    parent_collect = db['parents']

    try:
        user_collect.delete_one({'account': account})
        users_daily_games_collect.delete_one({'account': account})
        users_games_level_collect.delete_one({'account': account})
        users_games_records_collect.delete_one({'account': account})
        users_mission_collect.delete_one({'account': account})
        parent_collect.delete_one({'account': Paccount})

        resp = {
            'status': '200',
            'result': '',
            'msg': '刪除使用者成功'
        }
        return jsonify(resp)
    except Exception as err:
        resp = {
            'status': '404',
            'result': str(err),
            'msg': '刪除使用者成功錯誤'
        }
        return jsonify(resp)