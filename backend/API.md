# 啟動伺服器

* Use Flask：`python run.py`
* Use Gunicorn：`gunicorn -w 4 -b 127.0.0.1:5000 run:app`
* Use waitress：`python server.py`



# 資料庫 (MongoDB)

* **admins**

  ~~~json
  account: "", // 帳號
  pwd: "", // 密碼
  name: "", // 姓名
  authority: "" // 身份，admin
  ~~~

* **users**

  ~~~json
  account: "", // 帳號
  pwd: "", // 密碼
  name: "", // 測試者姓名
  authority: "", // 身份，userTest、userComp
  token: "" // [int] 獎勵點數
  ~~~

* **users_games_status**：紀錄測試者每個遊戲**下次要開始玩的level**

  ~~~json
  account: "",
  PrePet: "", // 正序寵物樂園, level 1~7
  BackPet: "", // 逆序寵物樂園, level 1~7
  PreAnimal: "", // 正序動物農莊, level 1~7
  BackAnimal: "", // 逆序動物農莊, level 1~7
  Teacher: "", // 老師點點名, level 1~4
  Where: "", // 橡果去哪兒, level 1~2
  Ball: "", // 球球滿天飛, level 1~8
  ~~~

* **comp_users_game_count**：紀錄對照組(控制組)是第幾次的順序，方便設置daily_games

  ~~~json
  _id: "0", 
  count: 0 // [int] 一週玩兩次，用來記錄game的順序
  ~~~

* **users_daily_games**：記錄測試者每天可以玩的遊戲及他有沒有完成 (每天00:00:01更新)

  ~~~json
  accout: "", // 測試者帳號
  complete: "", // [Boolean] 所有遊戲是否完成
  games: [{
    [gameNameEN]: { // 這個遊戲的遊戲名
      playTimes: "", // 這個遊戲玩的次數(最多2次，完成)
      complete: "", // [Boolean] 這個遊戲是否完成
    }
  }]
  ~~~

* **users_games_records**：紀錄測試者的遊玩紀錄

  ~~~json
  account: "", // 使用者帳號
  records: [{
      date: "", // [yyyy-mm-dd] 當天遊玩日期
      gameNameEN: "",
      level: "",
      respTime: "",
      trueRate: "",
      trueCount: ""
  }]
  ~~~

* **users_mission**：使用者的每日任務

  ~~~json
  account: "", // 使用者帳號
  loginMission: "", // [Boolean] 每日登入任務, 每日刷新,
  playMission: [] // [Array] 紀錄今天完成的gameNameEN
  ~~~

* **parents**：家長

  ~~~json
  account: "", // 家長帳號
  pwd: "", // 家長密碼
  name: "", // 家長姓名,
  phone: "", // 家長密碼,
  authority: "" // 家長身份, parentTest、parentComp
  childrenAccount: "", // 家長小孩的帳號
  questionnaires: [{
    "date": "", // [yyyy-mm-dd] 填問卷日期
    "focusValue": "", // 專注值
    "emotionValue": "", // 情緒值
    "motivationValue": "", // 動機值
    "feedback": "", // 回饋內容
  }]
  ~~~

* **feedbacks**：即時回饋

  ~~~json
  account: "", // 回饋者帳號
  date: "", // [yyyy-mm-dd] 日期,
  content: "" // 回饋內
  ~~~

* **gifts**：禮物列表

  ~~~json
  name: "", // 禮物名稱
  imgURL: "", // 禮物圖片url
  needToken: 0 // [int] 需要的token數量
  ~~~

* **gift_exchange**：禮物申請列表

  ~~~json
  studentAccount: "", // 申請人的帳號
  date: "", // [yyyy-mm-dd] 申請日期
  isGive: false // [boolean] 是否已經給禮物
  ~~~

* **week_count**：計算週次

  ~~~json
  _id: 0,
  week: 1 // [int] 代表現在是第幾週
  ~~~



# Restful API

* URL = https://hostname:8888/api/

* **Response Format**

  ~~~python
  resp = {
    "status": "", // 狀態碼
    "msg": "", // 訊息
    "result": "", // 回傳的資料
  }
  ~~~

* **Status Code**

  | Status Code | Description |
  | ----------- | ----------- |
  | 200         | 請求成功    |
  | 404         | 請求失敗    |

* **baseAPI**

  | API Method | API URL         | Desc             | Req Params    | Resp Result                                                  |
  | ---------- | --------------- | ---------------- | ------------- | ------------------------------------------------------------ |
  | POST       | URL/login       | 登入             | account, pwd  | name, account, authority (判斷身份。admin、userTest、userComp、parent) |
  | POST       | URL/logout      | 登出             |               |                                                              |
  | GET        | URL/checkLogin  | 檢查登入狀態     |               | status(boolean), authority, account                          |
  | GET        | URL/getUserInfo | 取得登入者的資料 |               | account, name, authority, phone                              |
  | GET        | URL/forgetPwd   | 忘記密碼取回     | name, account | pwd                                                          |

* **userAPI**：測試者

  | API Method | API URL                      | Desc                            | Req Params                                       | Resp Result                                                  |
  | ---------- | ---------------------------- | ------------------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
  | GET        | URL/user/getGames            | 取得當天可以練習的遊戲          |                                                  | [{gameNameCH, gameNameEN, imgURL, level, link, complete}]    |
  | GET        | URL/user/getLevel            | 取得所有遊戲的level             |                                                  | PrePet, BackPet, PreAnimal, BackAnimal, Teacher, Where, Ball |
  | POST       | URL/user/updateLevel         | 更新遊戲的level                 | gameNameEN, level                                |                                                              |
  | GET        | URL/user/getGameIsComplete   | 遊戲是否已完成                  | gameNameEN                                       | complete                                                     |
  | POST       | URL/user/updateTimesAndLevel | 更新每日遊戲可以玩的次數和level | gameNameEN                                       |                                                              |
  | POST       | URL/user/saveGameRecords     | 存遊玩紀錄                      | gameNameEN, level, respTime, trueRate, trueCount |                                                              |
  
* **adminAPI**：管理員

  | API Method | API URL                     | Desc                                        | Req Params                                                   | Resp Result                                                  |
  | ---------- | --------------------------- | ------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | GET        | URL/admin/getUsers          | 取得所有使用者結合家長的資料                |                                                              | [name, account, parentName, parentAccount, authority, phone] |
  | GET        | URL/admin/getTestUsers      | 取得實驗組使用者的資料                      |                                                              | account, name, phone                                         |
  | GET        | URL/admin/getCompUsers      | 取得對照組使用者的資料                      |                                                              | account, name, phone                                         |
  | GET        | URL/admin/getDailyUsersInfo | 取得每日所有users的資料以及有無完成每日遊戲 |                                                              | [{account, name, authority, complete}]                       |
  | GET        | URL/admin/getFeedback       | 取得請求日期的家長的回饋                    | date                                                         | [{chAccount, chName, pAccount, pName, pAuthority, focusValue, emotionValue, motivationValue, feedback}] |
  | POST       | URL/admin/addOneUser        | 增加一位使用者(user綁parent)                | authority, account, pwd, name, Pauthority(家長權限), Paccount(家長帳號), Ppwd(家長密碼), Pname(家長姓名), phone |                                                              |
  | POST       | URL/admin/delOneUser        | 刪除一位使用者(user綁parent)                | account, Paccount(家長帳號)                                  |                                                              |
  | POST       | URL/admin/addCsvUser        | 批次增加使用者                              | [{身份, 姓名, 帳號, 密碼, 家長姓名, 家長帳號, 家長密碼, 聯絡電話}] |                                                              |
  
* **parentAPI**：家長

  | API Method | API URL                  | Desc                    | Req Params                                          | Resp Result                                                  |
  | ---------- | ------------------------ | ----------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
  | GET        | URL/parent/checkDailyPSQ | 今天是否要做問卷        |                                                     | canDo(boolean), [如果已經做過問卷]=> focusValue, emotionValue, motivationValue, feedback |
  | POST       | URL/parent/sendPSQ       | 每日問卷                | focusValue, emotionValue, motivationValue, feedback |                                                              |
  | GET        | URL/parent/getChildGames | 取得當日孩子玩的遊戲    |                                                     | [{gameNameCH, gameNameEN, imgURL, level, link}]              |
  | GET        | URL/parent/getChildLevel | 取得孩子所有遊戲的level |                                                     | PrePet, BackPet, PreAnimal, BackAnimal, Teacher, Where, Ball |

* **tokenAPI**：獎勵點數

  | API Method | API URL                | Desc                                 | Req Params | Resp Result |
  | ---------- | ---------------------- | ------------------------------------ | ---------- | ----------- |
  | GET        | URL/token/getTokenNum  | 使用者的點數數量                     |            | token       |
  | POST       | URL/token/loginMission | 登入任務，完成任務+50                |            | addTokenNum |
  | POST       | URL/token/playMission  | 遊戲任務。完成遊戲+10，全部完成再+20 |            | addTokenNum |

* **dataAPI**：資料中心

  | API Method | API URL                 | Desc         | Req Params | Resp Result                                                  |
  | ---------- | ----------------------- | ------------ | ---------- | ------------------------------------------------------------ |
  | GET        | URL/data/user           | 使用者資料   |            | [{authority, name, account, pwd, token, parentName, parentAccount, parentPwd, phone}] |
  | GET        | URL/data/parent         | 家長資料     |            | [{authority, account, pwd, name, phone}]                     |
  | GET        | URL/data/admin          | 管理員資料   |            | [{name, account, pwd, authority}]                            |
  | GET        | URL/data/game           | 遊戲紀錄資料 |            | [{ account, records: [{date, gameNameEN, level, respTime, trueRate}] }] |
  | GET        | URL/data/questionnaires | 問卷資料     |            | [{ authority, account, name, parentAccount, parentName, questionnaires:[{date, focusValue, emotionValue, motivationValue, feedback}] }] |
  | GET        | URL/data/giftExchange   | 禮品兌換資料 |            | [{account, name, giftName, date, isGive}]                    |

* **giftAPI**：禮物

  | API Method | API URL                  | Desc         | Req Params | Resp Result                                                  |
  | ---------- | ------------------------ | ------------ | ---------- | ------------------------------------------------------------ |
  | GET        | URL/gift/getGifts        | 取得禮品列表 |            | [{name, imgURL, needToken}]                                  |
  | POST       | URL/gift/exchange        | 兌換禮品     | giftName   |                                                              |
  | GET        | URL/gift/exchangeRecords | 兌換禮品紀錄 |            | [{exchangeId, userAccount, userName, giftName, date, isGive}] |
  | POST       | URL/gift/sendGift        | 送出禮物     | exchangeId |                                                              |

* **rankAPI**：排名

  | API Method | API URL          | Desc             | Req Params | Resp Result                       |
  | ---------- | ---------------- | ---------------- | ---------- | --------------------------------- |
  | GET        | URL/rank/getRank | 取得金幣排名情況 | authority  | [{ranking, account, name, token}] |
  | GET        | URL/rank/getWeek | 取得訓練週次     |            | week                              |

  

