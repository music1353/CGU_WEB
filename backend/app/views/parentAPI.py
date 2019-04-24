from app import app
from config import MONGO_URI, BASE_DIR, client
from flask import jsonify, session, request
from datetime import datetime

# 連進MongoDB
db = client['cgu_db']

# 設置密鑰
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/api/parent/checkDailyPSQ', methods=['GET'])
def parent_check_daily_PSQ():
    '''家長今日是否需要做問卷
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [Boolean]canDo
            'msg': ''
        }
    '''

    collect = db['parents']
    doc = collect.find({'account': session['account']})

    flag = True
    date = datetime.now().strftime("%Y-%m-%d")
    list_doc = list(doc)
    questionnaires = list_doc[0]['questionnaires']

    obj = {
        'canDo': flag
    }

    for item in questionnaires:
        if item['date'] == date:
            flag = False

            obj['canDo'] = flag
            obj['focusValue'] = item['focusValue']
            obj['emotionValue'] = item['emotionValue']
            obj['motivationValue'] = item['motivationValue']
            obj['feedback'] = item['feedback']

    resp = {
        'status': '200',
        'result': obj,
        'msg': ''
    }
    return jsonify(resp)


@app.route('/api/parent/sendPSQ', methods=['POST'])
def parent_send_PSQ():
    '''家長填寫每日問卷
    Params:
        focusValue, emotionValue, motivationValue, feedback
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    date = datetime.now().strftime("%Y-%m-%d") # 今天日期
    focusValue = request.json['focusValue']
    emotionValue = request.json['emotionValue']
    motivationValue = request.json['motivationValue']
    feedback = request.json['feedback']

    obj = {
        'date': date,
        'focusValue': focusValue,
        'emotionValue': emotionValue,
        'motivationValue': motivationValue,
        'feedback': feedback
    }

    try:
        collect = db['parents']
        doc = collect.find_one_and_update({'account': session['account']}, {'$push': {'questionnaires': obj}})
        
        resp = {
            'status': '200',
            'result': '',
            'msg': '問卷新增成功'
        }
        return jsonify(resp)
    except Exception as err:
        resp = {
            'status': '404',
            'result': str(err),
            'msg': '問卷新增錯誤'
        }
        return jsonify(resp)
