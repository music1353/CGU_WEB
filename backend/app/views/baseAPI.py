from app import app
from config import MONGO_URI, BASE_DIR, client
from flask import jsonify, session, request

# 連進MongoDB
db = client['cgu_db']

# 設置密鑰
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/api/login', methods=['POST'])
def login():
    '''網頁端登入, 使用SESSION記錄登入
    Params:
        account: 登入帳號
        pwd: 登入密碼
    Returns:
        {
            'status': '200'->登入成功; '404'->登入失敗
            'result': name, account, authority
            'msg': ''
        }
    '''
    
    account = request.json['account']
    pwd = request.json['pwd']

    # 查看資料庫是否有此帳號
    user_collect = db['users']
    user_doc = user_collect.find_one({'account': account, 'pwd': pwd})

    admin_collect = db['admins']
    admin_doc = admin_collect.find_one({'account': account, 'pwd': pwd})

    parent_collect = db['parents']
    parent_doc = parent_collect.find_one({'account': account, 'pwd': pwd})

    if (user_doc is None) and (admin_doc is None) and (parent_doc is None):
        resp = {
            'status': '404',
            'result': '',
            'msg': '沒有此帳號'
        }
        return jsonify(resp)
    else:
        result_doc = ''
        if user_doc:
            result_doc = user_doc
        elif admin_doc:
            result_doc = admin_doc
        elif parent_doc:
            result_doc = parent_doc

        # 記錄到session
        session['login'] = True
        session['account'] = result_doc['account']
        session['authority'] = result_doc['authority']

        obj = {
            'name': result_doc['name'],
            'account': result_doc['account'],
            'authority': result_doc['authority']
        }

        resp = {
            'status': '200',
            'result': obj,
            'msg': '登入成功'
        }
        return jsonify(resp)


@app.route('/api/logout', methods=['POST'])
def logout():
    '''登出, 刪除SESSION內的紀錄
    Returns:
        {
            'status': '200'->登出成功
            'result': ''
            'msg': 訊息
        }
    '''

    if(session.get('login') != None):
        # 刪除session
        session.pop('login', None)
        session.pop('account', None)
        session.pop('authority', None)

        resp = {
            'status': '200',
            'result': '',
            'msg': '登出成功'
        }
        return jsonify(resp)
    else:
        resp = {
            'status': '404',
            'result': '',
            'msg': '原本就沒有此登入紀錄, 登出失敗'
        }
        return jsonify(resp)


@app.route('/api/checkLogin', methods=['GET'])
def checkLogin():
    '''檢查是否登入
    Returns:
        {
            'status': '200'->check成功; '404'->check發生錯誤
            'result': 正在登入的account; 錯誤訊息
            'msg': account登入中
        }
    '''

    try:
        if session.get('login') == True:
            obj = {
                'status': True,
                'authority': session['authority'],
                'account': session['account']
            }

            resp = {
                'status': '200',
                'result': obj,
                'msg': session['account']+'登入中'
            }
            return jsonify(resp)
        else:
            obj = {
                'status': False,
                'authority': '',
                'account': ''
            }

            resp = {
                'status': '200',
                'result': '',
                'msg': '未登入'
            }
            return jsonify(resp)
    except Exception as err:
        resp = {
            'status': '404',
            'result': str(err),
            'msg': '錯誤'
        }
        return jsonify(resp)


@app.route('/api/getUserInfo', methods=['GET'])
def get_user_info():
    '''取得登入者的資料
    Params:
        none
    Returns:
        {
            'status': '200'->登入成功; '404'->登入失敗
            'result': name, account, authority
            'msg': ''
        }
    '''

    obj = {}
    doc = {}
    if 'user' in session['authority']:
        collect = db['users']
        doc = collect.find_one({'account': session['account']})
    elif 'parent' in session['authority']:
        collect = db['parents']
        doc = collect.find_one({'account': session['account']})
    elif 'admin' in session['authority']:
        collect = db['admins']
        doc = collect.find_one({'account': session['account']})

    obj = {
        'name': doc['name'],
        'account': doc['account'],
        'authority': doc['authority']
    }

    resp = {
        'status': '200',
        'result': obj,
        'msg': '登入成功'
    }
    return jsonify(resp)