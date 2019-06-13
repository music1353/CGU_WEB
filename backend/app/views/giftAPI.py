from app import app
from config import MONGO_URI, client
from flask import jsonify, session, request
from datetime import datetime

# 連進MongoDB
db = client['cgu_db']

@app.route('/api/gift/getGifts', methods=['GET'])
def get_gifts():
    '''取得禮品列表
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{name, needToken}]
            'msg': ''
        }
    '''

    gift_collect = db['gifts']
    gift_doc = gift_collect.find({}, {'_id': False})

    resp = {
        'status': '200',
        'result': list(gift_doc),
        'msg': '取得禮品列表成功！'
    }
    return jsonify(resp)
    


@app.route('/api/gift/exchange', methods=['POST'])
def gift_exchange():
    '''小朋友兌換禮物
    Params:
        giftName
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    giftName = request.json['giftName']

    gift_collect = db['gifts']
    gift_doc = gift_collect.find_one({'name': giftName}, {'_id': False})
    
    # 修改使用者token
    needToken = gift_doc['needToken']
    user_collect = db['users']

    if 'Test' in session['authority']: # 實驗組needToken不變
        user_collect.find_one_and_update({'account': session['account']}, {'$inc': {'token': -needToken}})
    elif 'Comp' in session['authority']: # 對照組needToken*2/5
        user_collect.find_one_and_update({'account': session['account']}, {'$inc': {'token': -(needToken*2/5)}})
    
    user_doc = user_collect.find_one({'account': session['account']}, {'_id': False})

    # 取得最後一條exchangeId
    gift_exchange_collect = db['gift_exchange']
    new_gift_doc = gift_exchange_collect.find().sort([('exchangeId', -1)]).limit(1)
    lastId = list(new_gift_doc)[0]['exchangeId']

    # 加入exchange紀錄
    gift_exchange_collect = db['gift_exchange']
    exchange_obj = {
        'userAccount': session['account'],
        'exchangeId': lastId+1,
        'userName': user_doc['name'],
        'giftName': giftName,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'isGive': False
    }
    gift_exchange_collect.insert_one(exchange_obj)

    resp = {
        'status': '200',
        'result': '',
        'msg': '兌換禮品成功！'
    }
    return jsonify(resp)
    

@app.route('/api/gift/exchangeRecords', methods=['GET'])
def get_exchange_records():
    '''取得禮品列表
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{userAccount, giftName, date, isGive}]
            'msg': ''
        }
    '''

    gift_exchange_collect = db['gift_exchange']
    gift_exchange_doc = gift_exchange_collect.find({}, {'_id': False})
    ex_list = list(gift_exchange_doc)

    resp = {
        'status': '200',
        'result': ex_list,
        'msg': '取得兌換禮品紀錄成功！'
    }
    return jsonify(resp)


@app.route('/api/gift/sendGift', methods=['POST'])
def send_gift():
    '''送出禮物
    Params:
        exchangeId
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    exchangeId = request.json['exchangeId']
    
    gift_exchange_collect = db['gift_exchange']
    gift_exchange_collect.find_one_and_update({'exchangeId': exchangeId}, {'$set': {'isGive': True}})

    resp = {
        'status': '200',
        'result': '',
        'msg': '送出禮物成功！'
    }
    return jsonify(resp)
