from app import app
from config import MONGO_URI, client
from flask import jsonify, session, request
from datetime import datetime
from gameConfig import GAME_CH_NAME_DICT, GAME_IMG_DICT, LEVEL_CH_DICT

# 連進MongoDB
db = client['cgu_db']

# 設置密鑰
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/api/token/getTokenNum', methods=['GET'])
def token_get_token_num():
    '''取得使用者的點數數量
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': token
            'msg': ''
        }
    '''

    collect = db['users']
    doc = collect.find_one({'account': session['account']}, {'_id': False})

    resp = {
        'status': '200',
        'result': {
          'token': doc['token']
        },
        'msg': '取得使用者的點數數量成功!'
    }
    return jsonify(resp)  


@app.route('/api/token/loginMission', methods=['POST'])
def token_login_mission():
    '''登入任務，完成任務+50
    Params:
        None
    Returns:
        {
            'status': '200'->登入成功; '404'->登入失敗
            'result': addTokenNum
            'msg': ''
        }
    '''

    mission_collect = db['users_mission']
    mission_doc = mission_collect.find_one({'account': session['account']}, {'_id': False})

    if mission_doc['loginMission'] == False: # 今天登入任務還沒完成且登入 +50
        user_collect = db['users']
        user_collect.find_one_and_update({'account': session['account']}, {'$inc': {'token': 50}})
        mission_collect.find_one_and_update({'account': session['account']}, {'$set': {'loginMission': True}})

        resp = {
            'status': '200',
            'result': {
                'addTokenNum': 50
            },
            'msg': '完成登入任務 +50'
        }
        return jsonify(resp)
    else:
        resp = {
            'status': '404',
            'result': '',
            'msg': '今天已經完成登入任務'
        }
        return jsonify(resp)
        

@app.route('/api/token/playMission', methods=['POST'])
def token_play_mission():
    '''遊戲任務。完成遊戲+10，全部完成再+20
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->沒有遊戲可以玩
            'result': addTokenNum
            'msg': ''
        }
    '''

    user_collect = db['users']

    mission_collect = db['users_mission']
    mission_doc = mission_collect.find_one({'account': session['account']}, {'_id': False})

    games_collect = db['users_daily_games']
    games_doc = games_collect.find_one({'account': session['account']}, {'_id': False})

    # 看此遊戲是否complete, 若complete把gameNameEN加進playMission, +10
    if games_doc['games'] != []: # 今日有可玩的遊戲
        resp = {}
        for game in games_doc['games']:
            if game['complete']==True and (game['gameNameEN'] not in mission_doc['playMission']):
                # 把gameNameEN加進playMission
                mission_collect.update({'account': session['account']}, { '$push': { 'playMission': game['gameNameEN']}})
                # 增加token
                user_collect.find_one_and_update({'account': session['account']}, {'$inc': {'token': 10}})

                resp = {
                    'status': '200',
                    'result': {
                        'addTokenNum': 10
                    },
                    'msg': '完成遊戲任務'
                }
                break
            else:
                resp = {
                    'status': '200',
                    'result': {
                        'addTokenNum': 0
                    },
                    'msg': '完成遊戲任務'
                }

        if games_doc['complete'] == True: # 如果全部遊戲都玩完, +20
            user_collect.find_one_and_update({'account': session['account']}, {'$inc': {'token': 20}})
        
        return jsonify(resp)
    else:
        resp = {
            'status': '404',
            'result': '',
            'msg': '今天沒有遊戲可以玩'
        }
        return jsonify(resp)
