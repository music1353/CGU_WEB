import os
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
import atexit
from app import app
from config import client
from gameConfig import DB_GAMES_LIST, TEST_GAME_LIST
from app.modules.backup_engine.drive import drive


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

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
            # if dayOfWeek==5 or dayOfWeek==6: # 禮拜六日不用練習
            #     games = []
            #     doc['games'] = games
            # else: # 禮拜一 ~ 五
            #     games = DB_GAMES_LIST[dayOfWeek]
            #     doc['games'] = games

            ## 測試用
            games = TEST_GAME_LIST
            doc['games'] = games

            users_daily_games_collect.insert_one(doc)
            print('init', user['account'], 'complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
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
                comp_users_game_count_collect.find_one_and_update({'_id': '0'}, {'$set': {'count': count+1}})

            users_daily_games_collect.insert_one(doc)
            print('init', user['account'], 'complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def init_mission():
    db = client['cgu_db']
    collect = db['users_mission']
    
    try:
        collect.update({}, {'$set': {'loginMission': False}})
        print('init mission complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    except:
        print('init mission fail at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def backup():
    nowTime = datetime.now().strftime("%Y-%m-%d") # 今天日期

    # 創建資料夾
    try:
        mkdir_cmd = 'mkdir ./backup/' + nowTime
        os.system(mkdir_cmd)
        print('創建', nowTime, '資料夾成功！')
    except Exception as err:
        print('創建', nowTime, '資料夾失敗！')
        print('err:', err)

    # 備份每個collection的指令
    users_cmd = {
        'name': 'users',
        'cmd': 'mongoexport --db cgu_db --collection users --out ./backup/'+nowTime+'/users.json'
    }

    admins_cmd = {
        'name': 'admins',
        'cmd': 'mongoexport --db cgu_db --collection admins --out ./backup/'+nowTime+'/admins.json'
    }

    parents_cmd = {
        'name': 'parents',
        'cmd': 'mongoexport --db cgu_db --collection parents --out ./backup/'+nowTime+'/parents.json'
    }

    comp_users_game_count_cmd = {
        'name': 'comp_users_game_count',
        'cmd': 'mongoexport --db cgu_db --collection comp_users_game_count --out ./backup/'+nowTime+'/comp_users_game_count.json'
    }

    users_daily_games_cmd = {
        'name': 'users_daily_games',
        'cmd': 'mongoexport --db cgu_db --collection users_daily_games --out ./backup/'+nowTime+'/users_daily_games.json'
    }

    users_games_level_cmd = {
        'name': 'users_games_level',
        'cmd': 'mongoexport --db cgu_db --collection users_games_level --out ./backup/'+nowTime+'/users_games_level.json'
    }

    users_games_records_cmd = {
        'name': 'users_games_records',
        'cmd': 'mongoexport --db cgu_db --collection users_games_records --out ./backup/'+nowTime+'/users_games_records.json'
    }
    
    # 執行備份
    cmd_list = [users_cmd, admins_cmd, parents_cmd, comp_users_game_count_cmd, users_daily_games_cmd, users_games_level_cmd, users_games_records_cmd]
    for cmd in cmd_list:
        try:
            os.system(cmd['cmd'])
            print('backup', cmd['name'], 'collection complete at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        except Exception as err:
            print('backup', cmd['name'], 'error ! at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
            print('err:', err)


    # google drive 備份
    drive = drive()
    drive.backup()


scheduler = BackgroundScheduler()
scheduler.add_job(func=backup, trigger="cron", hour=7, minute=20, second=1)
scheduler.add_job(func=init_mission, trigger="cron", hour=15, minute=23, second=1)
scheduler.add_job(func=init_users_daily_games, trigger="cron", hour=8, minute=16, second=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    # app.run(use_reloader=False)
    app.run(debug=True) # 會執行兩次