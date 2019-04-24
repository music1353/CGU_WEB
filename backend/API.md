# 資料庫 (MongoDB)

* **users**

  ~~~json
  account: "", // 帳號
  pwd: "", // 密碼
  name: "", // 測試者姓名
  authority: "", // 身份，admin、userTest、userComp、parentTest、parentComp
  phone: "" // 聯絡電話
  ~~~

* **users_games_status**：紀錄測試者每個遊戲**下次要開始玩的level**

  ~~~json
  account: "",
  PrePet: "", // 正序寵物樂園, level 1~7
  BackPet: "", // 逆序寵物樂園, level 1~7
  PreAnimal: "", // 正序動物農莊, level 1~7
  BackAnimal: "", // 逆序動物農莊, level 1~7
  Teacher: "", // 老師點點名, level 1~4
  Where: "", // 橡果去哪兒, level 1~4
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
  complete: "", // [Bolean] 所有遊戲是否完成
  games: [{
    [gameNameEN]: { // 這個遊戲的遊戲名
      playTimes: "", // 這個遊戲玩的次數(最多2次，完成)
      complete: "", // [Bolean] 這個遊戲是否完成
    }
  }]
  ~~~

* **users_games_records**：紀錄測試者的遊玩紀錄

  ~~~json
  account: "", // 測試者帳號
  records: [{
      date: "", // [yyyy-mm-dd] 當天遊玩日期
      gameNameEN: "",
      level: "",
      respTime: "",
      trueRate: "",
      trueCount: ""
  }]
  ~~~

* **parents**：紀錄家長的每日問卷

  ~~~json
  account: "", //家長帳號
  childrenAccount: "", //家長小孩的帳號
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
  content: "" // 回饋內容
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

  | API Method | API URL         | Desc             | Req Params   | Resp Result                                                  |
  | ---------- | --------------- | ---------------- | ------------ | ------------------------------------------------------------ |
  | POST       | URL/login       | 登入             | account, pwd | name, account, authority (判斷身份。admin、userTest、userComp、parent) |
  | POST       | URL/logout      | 登出             |              |                                                              |
  | GET        | URL/checkLogin  | 檢查登入狀態     |              | status(boolean), authority, account                          |
  | GET        | URL/getUserInfo | 取得登入者的資料 |              | account, name, authority, phone                              |

* **userAPI**：測試者

  | API Method | API URL                      | Desc                            | Req Params                                       | Resp Result                                                  |
  | ---------- | ---------------------------- | ------------------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
  | GET        | URL/user/getGames            | 取得當天可以練習的遊戲          |                                                  | [{gameNameCH, gameNameEN, imgURL, reviews, link}]            |
  | GET        | URL/user/getLevel            | 取得所有遊戲的level             |                                                  | PrePet, BackPet, PreAnimal, BackAnimal, Teacher, Where, Ball |
  | POST       | URL/user/updateLevel         | 更新遊戲的level                 | gameNameEN, level                                |                                                              |
  | GET        | URL/user/getGameIsComplete   | 遊戲是否已完成                  | gameNameEN                                       | complete                                                     |
  | POST       | URL/user/updateTimesAndLevel | 更新每日遊戲可以玩的次數和level | gameNameEN                                       |                                                              |
  | POST       | URL/user/saveGameRecords     | 存遊玩紀錄                      | gameNameEN, level, respTime, trueRate, trueCount |                                                              |

* **adminAPI**：管理員

  | API Method | API URL                     | Desc                                        | Req Params | Resp Result                                                  |
  | ---------- | --------------------------- | ------------------------------------------- | ---------- | ------------------------------------------------------------ |
  | GET        | URL/admin/getUsers          | 取得所有使用者的資料                        |            | account, name, authority, phone                              |
  | GET        | URL/admin/getTestUsers      | 取得實驗組使用者的資料                      |            | account, name, phone                                         |
  | GET        | URL/admin/getCompUsers      | 取得對照組使用者的資料                      |            | account, name, phone                                         |
  | GET        | URL/admin/getDailyUsersInfo | 取得每日所有users的資料以及有無完成每日遊戲 |            | [{account, name, authority, complete}]                       |
  | GET        | URL/admin/getFeedback       | 取得請求日期的家長的回饋                    | date       | [{chAccount, chName, pAccount, pName, pAuthority, focusValue, emotionValue, motivationValue, feedback}] |

* **parentAPI**：家長

  | API Method | API URL                  | Desc             | Req Params                                          | Resp Result                                                  |
  | ---------- | ------------------------ | ---------------- | --------------------------------------------------- | ------------------------------------------------------------ |
  | GET        | URL/parent/checkDailyPSQ | 今天是否要做問卷 |                                                     | canDo(boolean), [如果已經做過問卷]=> focusValue, emotionValue, motivationValue, feedback |
  | POST       | URL/parent/sendPSQ       | 每日問卷         | focusValue, emotionValue, motivationValue, feedback |                                                              |
  |            |                          |                  |                                                     |                                                              |

  