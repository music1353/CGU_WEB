from app import app
from config import MONGO_URI, client
from flask import jsonify, session, request
from datetime import datetime
from gameConfig import GAME_CH_NAME_DICT, GAME_IMG_DICT, LEVEL_CH_DICT

# 連進MongoDB
db = client['cgu_db']

@app.route('/api/user/getGames', methods=['GET'])
def user_get_games():
    '''取得當天可以練習的遊戲
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': [{gameNameCH, gameNameEN, imgURL, level, link}]
            'msg': ''
        }
    '''

    games_collect = db['users_daily_games']
    games_doc = games_collect.find_one({'account': session['account']}, {'_id': False})

    level_collect = db['users_games_level']
    level_doc = level_collect.find_one({'account': session['account']}, {'_id': False})

    games = []
    if games_doc['games'] != []: # 今日有可玩的遊戲
        for game in games_doc['games']:
            nameEN = game['gameNameEN']
            obj = {
                'gameNameCH': GAME_CH_NAME_DICT[nameEN],
                'gameNameEN': nameEN,
                'imgURL': GAME_IMG_DICT[nameEN],
                'level': LEVEL_CH_DICT[level_doc[nameEN]],
                'link': 'game/'+nameEN+'_'+level_doc[nameEN],
                'complete': game['complete']
            }
            games.append(obj)
    else: # 今日沒有可玩的遊戲
        print('今日沒有可玩的遊戲 -- from user/getGames')

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
    

@app.route('/api/user/getLevel', methods=['GET'])
def user_get_level():
    '''取得測試者所有遊戲的level
    Params:
        none
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': 各個遊戲的level
            'msg': ''
        }
    '''

    collect = db['users_games_level']
    users_games_level_doc = collect.find_one({'account': session['account']}, {'_id': False})

    resp = {
        'status': '200',
        'result': users_games_level_doc,
        'msg': '遊戲請求成功'
    }
    return jsonify(resp)


@app.route('/api/user/getGameIsComplete', methods=['GET'])
def user_get_is_complete():
    '''取得遊戲是否已完成
    Params:
        gameNameEN
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': complete
            'msg': ''
        }
    '''
    gameNameEN = request.args.get("gameNameEN")

    collect = db['users_daily_games']
    doc = collect.find_one({'account': session['account']}, {'_id': False})
    games = doc['games']

    flag = False
    for game in games:
        if game['gameNameEN'] == gameNameEN:
            flag = game['complete']

    resp = {
        'status': '200',
        'result': {'complete': flag},
        'msg': gameNameEN+'取得遊戲是否已完成成功'
    }
    return jsonify(resp)


@app.route('/api/user/updateTimesAndLevel', methods=['POST'])
def user_update_game_time():
    '''更新每日遊戲可以玩的次數跟level
    Params:
        gameNameEN, level(現在玩完的level), trueRate
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    gameNameEN = request.json['gameNameEN']
    level = request.json['level']
    trueRate = request.json['trueRate']

    users_daily_games_collect = db['users_daily_games']
    users_daily_games_doc = users_daily_games_collect.find_one({'account': session['account']}, {'_id': False})
    games = users_daily_games_doc['games']

    # 更新請求的遊戲的遊玩次數
    newGames = []
    playTimes = 0 # 為了更新level
    for game in games:
        if game['gameNameEN'] == gameNameEN:
            playTimes = game['playTimes'] # 為了更新level
            if game['playTimes'] == '1':
                obj = {
                    'gameNameEN': gameNameEN,
                    'playTimes': '0',
                    'complete': True
                }
                newGames.append(obj)
            else:
                obj = {
                    'gameNameEN': gameNameEN,
                    'playTimes': str(int(game['playTimes'])-1),
                    'complete': False
                }
                newGames.append(obj)
        else:
            newGames.append(game)

    users_daily_games_collect.find_one_and_update({'account': session['account']}, {'$set': {'games': newGames}}, {'_id': False})

    # 更新level
    users_games_level_collect = db['users_games_level']

    # 取得現在遊戲的level, 防止變成0跟超過最高level
    users_games_level_doc = users_games_level_collect.find_one({'account': session['account']}, {'_id': False})
    nowLevel = users_games_level_doc[gameNameEN]

    if float(trueRate) >= 80: # 有過80%, 升級
        # 升級+20token
        user_collect = db['users']
        user_collect.find_one_and_update({'account': session['account']}, {'$inc': {'token': 20}})

        # 升級levelUpTimesMission+1
        user_mission_collect = db['users_mission']
        user_mission_collect.find_one_and_update({'account': session['account']}, {'$inc': {'levelUpTimesMission': 1}})
        
        # 若已經是最高level, 不更改level
        if nowLevel=='7' and (gameNameEN=='PrePet' or gameNameEN=='BackPet' or gameNameEN=='PreAnimal' or gameNameEN=='BackAnimal'):
            print(gameNameEN, '的最高級是7,', '現在遊玩level是', nowLevel, ', 所以不改level')
            pass
        elif nowLevel=='4' and gameNameEN=='Teacher':
            print(gameNameEN, '的最高級是4,', '現在遊玩level是', nowLevel, ', 所以不改level')
            pass
        elif nowLevel=='3' and gameNameEN=='Where':
            print(gameNameEN, '的最高級是3,', '現在遊玩level是', nowLevel, ', 所以不改level')
            pass
        elif nowLevel=='8' and gameNameEN=='Ball':
            print(gameNameEN, '的最高級是8,', '現在遊玩level是', nowLevel, ', 所以不改level')
            pass
        else:
            if playTimes == '2': # 第一次玩, 下一次level+1
                users_games_level_collect.find_one_and_update({'account': session['account']}, {'$set': {gameNameEN: str(int(level)+1)}}, upsert=False)
            elif playTimes == '1': # 第二次玩, 下一次重疊level開始
                users_games_level_collect.find_one_and_update({'account': session['account']}, {'$set': {gameNameEN: level}}, upsert=False)
    elif float(trueRate) < 80: # 沒過80%降級, 動物農莊、寵物樂園playTimes-1, 其他playTimes歸0
        # 降級, 如果level是1就不降
        if nowLevel == '1':
            print('因為現在level是', nowLevel, '不降級')
            pass
        else:
            users_games_level_collect.find_one_and_update({'account': session['account']}, {'$set': {gameNameEN: str(int(level)-1)}}, upsert=False)

        # 動物農莊、寵物樂園playTimes-1, 其他playTimes歸0
        newGames = []
        for game in games:
            if game['gameNameEN'] == gameNameEN:
                # 如果是動物農莊或寵物樂園, playTimes降一級
                if gameNameEN=='PreAnimal' or gameNameEN=='BackAnimal' or gameNameEN=='PrePet' or gameNameEN=='BackPet':
                    if game['playTimes'] == '1': # 剩下一次遊戲次數, 玩玩這次就結束
                        obj = {
                            'gameNameEN': gameNameEN,
                            'playTimes': str(int(playTimes)-1),
                            'complete': True
                        }
                        newGames.append(obj)
                    else: # 還可以玩
                        obj = {
                            'gameNameEN': gameNameEN,
                            'playTimes': str(int(playTimes)-1),
                            'complete': False
                        }
                        newGames.append(obj)
                # 其他遊戲playTimes歸0
                else:
                    obj = {
                        'gameNameEN': gameNameEN,
                        'playTimes': '0',
                        'complete': True
                    }
                    newGames.append(obj)
            else:
                newGames.append(game)

        users_daily_games_collect.find_one_and_update({'account': session['account']}, {'$set': {'games': newGames}},{'_id': False})
    

    # 更新看是否所有遊戲是否都已完成, 更新今日整體的complete
    flag = True
    doc = users_daily_games_collect.find_one({'account': session['account']}, {'_id': False})
    games = doc['games']
    for game in games:
        if game['complete'] == False:
            flag = False
    users_daily_games_collect.find_one_and_update({'account': session['account']}, {'$set': {'complete': flag}}, {'_id': False})


    resp = {
        'status': '200',
        'result': '',
        'msg': gameNameEN+'更新遊戲次數成功'
    }
    return jsonify(resp)


@app.route('/api/user/saveGameRecords', methods=['POST'])
def user_save_game_records():
    '''存遊戲的遊玩紀錄
    Params:
        gameNameEN, level, respTime, trueRate, trueCount
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''

    gameNameEN = request.json['gameNameEN']
    level = request.json['level']
    respTime = request.json['respTime']
    trueRate = request.json['trueRate']
    trueCount = request.json['trueCount']
    endTime = request.json['endTime']

    collect = db['users_games_records']
    date = datetime.now().strftime("%Y-%m-%d") # 今天日期
    
    # 把紀錄放進date內
    obj = {
        'date': date,
        'gameNameEN': gameNameEN,
        'level': level
    }

    if respTime != 'X':
        obj['respTime'] = respTime
    if trueRate != 'X':
        obj['trueRate'] = trueRate
    if trueCount != 'X':
        obj['trueCount'] = trueCount

    # 計算遊玩時間
    users_train_time_collect = db['users_train_time']
    users_train_time_doc = users_train_time_collect.find_one({'account': session['account']}, {'_id': False})
    ## 計算時間差
    startTime = datetime.strptime(users_train_time_doc['startTime'], "%Y-%m-%d %H:%M:%S")
    endTime =  datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    train_time_in_sec = (endTime - startTime).seconds
    obj['startTime'] = users_train_time_doc['startTime']
    obj['trainTime'] = train_time_in_sec

    try:
        collect.find_one_and_update({'account': session['account']}, {'$push': {'records': obj}},{'_id': False})
        
        resp = {
            'status': '200',
            'result': '',
            'msg': gameNameEN+' level'+level+'，遊戲紀錄成功'
        }
        return jsonify(resp)
    except Exception as err:
        resp = {
            'status': '404',
            'result': str(err),
            'msg': gameNameEN+' level'+level+'，遊戲紀錄失敗'
        }
        return jsonify(resp)
    

@app.route('/api/user/dailyMission', methods=['GET'])
def user_daily_mission():
    '''取得使用者每日任務的進度
    Params:
        None
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': loginMission, allCompleteMission, completeGameTimes, levelUpTimesMission
            'msg': ''
        }
    '''

    collect = db['users_mission']
    doc = collect.find_one({'account': session['account']}, {'_id': False})

    completeGameTimes = len(doc['playMission'])

    result = {
        'loginMission': doc['loginMission'],
        'allCompleteMission': doc['allCompleteMission'],
        'completeGameTimes': completeGameTimes,
        'levelUpTimesMission': doc['levelUpTimesMission']
    }

    resp = {
        'status': '200',
        'result': result,
        'msg': '取得使用者每日任務的進度成功'
    }
    return jsonify(resp)


@app.route('/api/user/setTrainTime', methods=['POST'])
def user_set_train_time():
    '''紀錄正在訓練遊戲的開始時間
    Params:
        gameNameEN, startTime
    Returns:
        {
            'status': '200'->成功; '404'->失敗
            'result': ''
            'msg': ''
        }
    '''
    gameNameEN = request.json['gameNameEN']
    startTime = request.json['startTime']
    
    collect = db['users_train_time']
    # 如果沒有此用戶, 建立一個此用戶的doc
    doc = collect.find_one({'account': session['account']}, {'_id': False})
    if doc == None:
        obj = {
            'account': session['account'],
            'gameNameEN': '',
            'startTime': ''
        }
        collect.insert(obj);
        print(session['account'], '在users_train_time沒有doc, 創立新doc成功!')
        doc = collect.find_one({'account': session['account']}, {'_id': False}) # 再找一次
    else:
        pass # has the user's doc

    collect.find_one_and_update({'account': session['account']}, {'$set': {'gameNameEN': gameNameEN, 'startTime': startTime}})

    resp = {
        'status': '200',
        'result': '',
        'msg': '紀錄正在訓練遊戲的開始時間成功'
    }
    return jsonify(resp)