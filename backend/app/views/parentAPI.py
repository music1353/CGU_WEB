from app import app
from config import MONGO_URI, client
from flask import jsonify, session, request
from datetime import datetime
from gameConfig import GAME_CH_NAME_DICT, GAME_IMG_DICT, LEVEL_CH_DICT

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


@app.route('/api/parent/getChildGames', methods=['GET'])
def parent_get_child_games():
    '''取得當日孩子玩的遊戲
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{gameNameCH, gameNameEN, imgURL, level, link}]
            'msg': ''
        }
    '''

    parent_collect = db['parents']
    parent_doc = parent_collect.find_one({'account': session['account']}, {'_id': False})
    child_account = parent_doc['childrenAccount']

    games_collect = db['users_daily_games']
    games_doc = games_collect.find({'account': child_account}, {'_id': False})

    level_collect = db['users_games_level']
    level_doc = level_collect.find_one({'account': child_account}, {'_id': False})

    games = []
    games_doc_list = list(games_doc)
    
    if games_doc_list[0]['games'] != []: # 今日有可玩的遊戲
        # 取得gameNameEN
        temp = []
        for item in games_doc_list[0]['games']:
            temp.append(item['gameNameEN'])

        # 加上中文名字跟imgUrl
        for nameEN in temp:
            obj = {
                'gameNameCH': GAME_CH_NAME_DICT[nameEN],
                'gameNameEN': nameEN,
                'imgURL': GAME_IMG_DICT[nameEN],
                'level': LEVEL_CH_DICT[level_doc[nameEN]],
                'link': 'game/'+nameEN+'_'+level_doc[nameEN]
            }
            games.append(obj)
    else: # 今日沒有可玩的遊戲
        print('今日沒有可玩的遊戲')

    # 用msg表達今天有無遊戲要玩
    resp = {}
    if games==[]:
        resp = {
            'status': '200',
            'result': games,
            'msg': False
        }
    else:
        resp = {
            'status': '200',
            'result': games,
            'msg': True
        }
    return jsonify(resp)   


@app.route('/api/parent/getChildLevel', methods=['GET'])
def parent_get_child_level():
    '''取得孩子所有遊戲的level
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': 各個遊戲的level
            'msg': ''
        }
    '''

    parent_collect = db['parents']
    parent_doc = parent_collect.find_one({'account': session['account']}, {'_id': False})
    child_account = parent_doc['childrenAccount']
    
    collect = db['users_games_level']
    users_games_level_doc = collect.find_one({'account': child_account}, {'_id': False})

    obj = [{
        'gameNameEN': 'PrePet',
        'gameNameCH': '正序寵物樂園',
        'level': LEVEL_CH_DICT[users_games_level_doc['PrePet']],
        'highlight': False
    }, {
        'gameNameEN': 'BackPet',
        'gameNameCH': '逆序寵物樂園',
        'level': LEVEL_CH_DICT[users_games_level_doc['BackPet']],
        'highlight': False
    }, {
        'gameNameEN': 'PreAnimal',
        'gameNameCH': '正序動物農莊',
        'level': LEVEL_CH_DICT[users_games_level_doc['PreAnimal']],
        'highlight': False
    }, {
        'gameNameEN': 'BackAnimal',
        'gameNameCH': '逆序動物農莊',
        'level': LEVEL_CH_DICT[users_games_level_doc['BackAnimal']],
        'highlight': False
    }, {
        'gameNameEN': 'Teacher',
        'gameNameCH': '老師點點名',
        'level': LEVEL_CH_DICT[users_games_level_doc['Teacher']],
        'highlight': False
    }, {
        'gameNameEN': 'Where',
        'gameNameCH': '橡果去哪兒',
        'level': LEVEL_CH_DICT[users_games_level_doc['Where']],
        'highlight': False
    }, {
        'gameNameEN': 'Ball',
        'gameNameCH': '球球滿天飛',
        'level': LEVEL_CH_DICT[users_games_level_doc['Ball']],
        'highlight': False
    }]

    resp = {
        'status': '200',
        'result': obj,
        'msg': '孩子遊戲level請求成功'
    }
    return jsonify(resp)