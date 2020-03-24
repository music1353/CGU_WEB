import time
from datetime import datetime
from gameConfig import DB_GAMES_LIST, TEST_GAME_LIST, USER_DISPLAY_GAME_LIST
from config import client
import os
from app.modules.backup_engine.drive import drive
from app.modules.backup_engine import local

# 確認APScheduler還活著
def check_scheduler_alive():
    print('keep alive...APScheduler...zz')

# 更新週次, 如果是禮拜一, week+1
def update_week(): 
    db = client['cgu_db']
    collect = db['week_count']

    if datetime.now().weekday() == 0: # 星期一
        collect.find_one_and_update({'_id': 0}, {'$inc': {'week': 1}})
        print('update week complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# 更新每日任務
def init_mission():
    db = client['cgu_db']
    collect = db['users_mission']

    try:
        collect.update_many({}, {'$set': {'loginMission': False, 'allCompleteMission': False, 'playMission': [], 'levelUpTimesMission': 0}})
        print('init mission complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    except Exception as err:
        print('init mission fail at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        print(err)



# 更新每日訓練遊戲
def init_users_daily_games():
    db = client['cgu_db']

    # users collection
    users_collect = db['users']
    user_doc = users_collect.find({})

    # users_daily_games collection
    users_daily_games_collect = db['users_daily_games']
    users_daily_games_collect.remove()
    print('remove users_daily_games collection complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    dayOfWeek = datetime.now().weekday() # 今天星期幾 0~6
    print('dayOfWeek:', dayOfWeek)

    for user in list(user_doc):
        doc = {
            'account': user['account'],
            'complete': False,
            'games': []
        }

        if user['authority'] == 'userTest': # 實驗組
            if dayOfWeek==5 or dayOfWeek==6: # 禮拜六日不用練習
                games = []
                doc['games'] = games
            else: # 禮拜一 ~ 五
                games = DB_GAMES_LIST[dayOfWeek]
                doc['games'] = games

            users_daily_games_collect.insert_one(doc)
            print('init', user['account'], 'complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

            ## 測試用
            # games = TEST_GAME_LIST
            # doc['games'] = games

            # users_daily_games_collect.insert_one(doc)
            # print('init', user['account'], 'complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        elif user['authority'] == 'userComp': # 對照組(控制組)
            comp_users_game_count_collect = db['comp_users_game_count']
            comp_users_game_count_doc = comp_users_game_count_collect.find({'_id': '0'})
            doc_list = list(comp_users_game_count_doc)
            count = int(doc_list[0]['count'])

            if dayOfWeek==0 or dayOfWeek==2 or dayOfWeek==3 or dayOfWeek==5 or dayOfWeek==6: # 禮拜ㄧ、三、四、六、七，不用練習
                games = []
                doc['games'] = games
            else: # 禮拜二、五要練習
                games = DB_GAMES_LIST[count%5]
                doc['games'] = games
            
            users_daily_games_collect.insert_one(doc)
            print('init', user['account'], 'complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

        # FIXME: 20200310 展示用, 一～日都有遊戲
        elif user['authority'] == 'userDisplay':
            # comp_users_game_count_collect = db['comp_users_game_count']
            # comp_users_game_count_doc = comp_users_game_count_collect.find_one({'id': '1'})
            # count = comp_users_game_count_doc['count']

            games = USER_DISPLAY_GAME_LIST
            doc['games'] = games
            users_daily_games_collect.insert_one(doc)
            print('init', user['account'], 'complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    # 禮拜二、五要練習 => 對照組 comp_users_game_count+1
    if dayOfWeek==1 or dayOfWeek==4: # 禮拜二、五
        comp_users_game_count_collect.find_one_and_update({'_id': '0'}, {'$inc': {'count': 1}})

    # FIXME: 20200310 展示用, 一～日都有遊戲
    # comp_users_game_count_collect.find_one_and_update({'id': '1'}, {'$inc': {'count': 1}})



# TODO: 紀錄每日的users_complete_records(紀錄每天是否完成任務)
def insert_users_complete_records():
    db = client['cgu_db']
    week_count_collect = db['week_count']
    week_count_doc = week_count_collect.find_one({'_id': 0})

    nowWeek = week_count_doc['week'] # 這週週次
    nowTime = datetime.now().strftime("%Y-%m-%d") # 今天日期
    
    users_mission_collect = db['users_mission']
    users_complete_records_collect = db['users_complete_records']
    users_daily_games_collect = db['users_daily_games']

    users_mission_doc = users_mission_collect.find({})
    for user in list(users_mission_doc):
        # 先檢查今天是否有遊戲需要訓練，有的話才紀錄
        users_daily_games_doc = users_daily_games_collect.find_one({'account': user['account']}, {'_id': False})

        if len(users_daily_games_doc['games'])>0: # 當天有訓練遊戲
            obj = {
                'date': nowTime,
                'week': nowWeek,
                'loginMission': user['loginMission'],
                'allCompleteMission': user['allCompleteMission'],
            }
            users_complete_records_collect.find_one_and_update({'account': user['account']}, {'$push': {'records': obj}},{'_id': False})
            print('insert', user['account'], 'records complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        else: # 當天不用訓練
            print(user['account'], '當天不用訓練遊戲！')

# google cloud備份
def cloud_backup():
    # google drive 備份
    googledrive = drive()
    googledrive.backup()


# 本地備份
def local_backup():
    local.run_backup()

    # 在有mongo env下才能下mongoexport指令
    # nowTime = datetime.now().strftime("%Y-%m-%d") # 今天日期

    # # 創建資料夾
    # try:
    #     mkdir_cmd = 'mkdir ./backup/' + nowTime # in linux
    #     # mkdir_cmd = 'mkdir .\\backup\\' + nowTime # in win
    #     os.system(mkdir_cmd)
    #     print('創建', nowTime, '資料夾成功！')
    # except Exception as err:
    #     print('創建', nowTime, '資料夾失敗！')
    #     print('err:', err)

    # # 備份每個collection的指令
    # users_cmd = {
    #     'name': 'users',
    #     'cmd': './mongoexport --db cgu_db --collection users --out ./backup/'+nowTime+'/users.json'
    # }

    # admins_cmd = {
    #     'name': 'admins',
    #     'cmd': './mongoexport --db cgu_db --collection admins --out ./backup/'+nowTime+'/admins.json'
    # }

    # parents_cmd = {
    #     'name': 'parents',
    #     'cmd': './mongoexport --db cgu_db --collection parents --out ./backup/'+nowTime+'/parents.json'
    # }

    # comp_users_game_count_cmd = {
    #     'name': 'comp_users_game_count',
    #     'cmd': './mongoexport --db cgu_db --collection comp_users_game_count --out ./backup/'+nowTime+'/comp_users_game_count.json'
    # }

    # users_daily_games_cmd = {
    #     'name': 'users_daily_games',
    #     'cmd': './mongoexport --db cgu_db --collection users_daily_games --out ./backup/'+nowTime+'/users_daily_games.json'
    # }

    # users_games_level_cmd = {
    #     'name': 'users_games_level',
    #     'cmd': './mongoexport --db cgu_db --collection users_games_level --out ./backup/'+nowTime+'/users_games_level.json'
    # }

    # users_games_records_cmd = {
    #     'name': 'users_games_records',
    #     'cmd': './mongoexport --db cgu_db --collection users_games_records --out ./backup/'+nowTime+'/users_games_records.json'
    # }

    # # TODO:
    # users_complete_records_cmd = {
    #     'name': 'users_complete_records',
    #     'cmd': './mongoexport --db cgu_db --collection users_complete_records --out ./backup/'+nowTime+'/users_complete_records.json'
    # }

    # users_mission_cmd = {
    #     'name': 'users_mission',
    #     'cmd': './mongoexport --db cgu_db --collection users_mission --out ./backup/'+nowTime+'/users_mission.json'
    # }

    # gifts_cmd = {
    #     'name': 'gifts',
    #     'cmd': './mongoexport --db cgu_db --collection gifts --out ./backup/'+nowTime+'/gifts.json'
    # }

    # gift_exchange_cmd = {
    #     'name': 'gift_exchange',
    #     'cmd': './mongoexport --db cgu_db --collection gift_exchange --out ./backup/'+nowTime+'/gift_exchange.json'
    # }

    # week_count_cmd = {
    #     'name': 'week_count',
    #     'cmd': './mongoexport --db cgu_db --collection week_count --out ./backup/'+nowTime+'/week_count.json'
    # }
    
    # # 執行備份
    # cmd_list = [users_cmd, admins_cmd, parents_cmd, comp_users_game_count_cmd, users_daily_games_cmd, users_games_level_cmd, users_games_records_cmd, users_complete_records_cmd, users_mission_cmd, gifts_cmd, gift_exchange_cmd, week_count_cmd]
    # for cmd in cmd_list:
    #     try:
    #         os.system(cmd['cmd'])
    #         print('backup', cmd['name'], 'collection complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    #     except Exception as err:
    #         print('backup', cmd['name'], 'error ! at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    #         print('err:', err)