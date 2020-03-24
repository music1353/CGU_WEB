from config import client, BASE_DIR, MODULE_DIR
from gameConfig import DB_GAMES_LIST, USER_DISPLAY_GAME_LIST
from datetime import datetime

# params: auth
# return: [array] games
def set_game(auth):
    db = client['cgu_db']
    games = [] # return 今天的所有遊戲
    dayOfWeek = datetime.now().weekday() # 今天星期幾 0~6

    if auth == 'userTest': # 實驗組
        if dayOfWeek==5 or dayOfWeek==6: # 禮拜六日不用練習
            games = []
        else: # 禮拜一 ~ 五
            games = DB_GAMES_LIST[dayOfWeek]
    elif auth == 'userComp': # 對照組(控制組)
        comp_users_game_count_collect = db['comp_users_game_count']
        comp_users_game_count_doc = comp_users_game_count_collect.find_one({'_id': '0'})
        count = comp_users_game_count_doc['count']
        # doc_list = list(comp_users_game_count_doc)
        # count = int(doc_list[0]['count'])

        if dayOfWeek==0 or dayOfWeek==2 or dayOfWeek==3 or dayOfWeek==5 or dayOfWeek==6: # 禮拜ㄧ、三、四、六、七，不用練習
            games = []
        else: # 禮拜二、五要練習
            games = DB_GAMES_LIST[count%5]

    # FIXME: 20200310 展示用, 一～日都有遊戲
    elif auth == 'userDisplay':
        # comp_users_game_count_collect = db['comp_users_game_count']
        # comp_users_game_count_doc = comp_users_game_count_collect.find_one({'id': '1'})
        # count = comp_users_game_count_doc['count']

        games = USER_DISPLAY_GAME_LIST

    
    return games