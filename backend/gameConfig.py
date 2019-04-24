# games代號列表 => FOR DB
DB_GAMES_LIST = [
    [ # 第一種組合 ADE
        { 
            'gameNameEN': 'PrePet',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'BackAnimal',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Teacher',
            'playTimes': '2',
            'complete': False
        }
    ],
    [ # 第二種組合 BCF
        {
            'gameNameEN': 'BackPet',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'PreAnimal',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Ball',
            'playTimes': '2',
            'complete': False
        }
    ],
    [ # 第三種組合 ACG
        {
            'gameNameEN': 'PrePet',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'PreAnimal',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Where',
            'playTimes': '2',
            'complete': False
        }
    ],
    [ # 第四種組合 DEF
        {
            'gameNameEN': 'BackAnimal',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Teacher',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Ball',
            'playTimes': '2',
            'complete': False
        }
    ],
    [ # 第五種組合 BEG
        {
            'gameNameEN': 'BackPet',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Teacher',
            'playTimes': '2',
            'complete': False
        }, {
            'gameNameEN': 'Where',
            'playTimes': '2',
            'complete': False
        }
    ]
]


## 測試用
TEST_GAME_LIST = [
    {
        'gameNameEN': 'BackPet',
        'playTimes': '2',
        'complete': False
    }, {
        'gameNameEN': 'PreAnimal',
        'playTimes': '2',
        'complete': False
    }, {
        'gameNameEN': 'Ball',
        'playTimes': '2',
        'complete': False
    }
]



# games中文名字、imgURL對照表 => FOR CLIENT
GAME_CH_NAME_DICT = {
    'PrePet': '正序寵物樂園',
    'BackPet': '後序寵物樂園',
    'PreAnimal': '正序動物農莊',
    'BackAnimal': '後序動物農莊',
    'Teacher': '老師點點名',
    'Ball': '球球滿天飛',
    'Where': '橡果去哪兒'
}

GAME_IMG_DICT = {
    'PrePet': '/static/game_pictures/pet.jpg',
    'BackPet': '/static/game_pictures/pet.jpg',
    'PreAnimal': '/static/game_pictures/animal.jpg',
    'BackAnimal': '/static/game_pictures/animal.jpg',
    'Teacher': '/static/game_pictures/teacher.jpg',
    'Ball': '/static/game_pictures/ball.jpg',
    'Where': '/static/game_pictures/where.jpg'
}

LEVEL_CH_DICT = {
    '1': '第一關卡',
    '2': '第二關卡',
    '3': '第三關卡',
    '4': '第四關卡',
    '5': '第五關卡',
    '6': '第六關卡',
    '7': '第七關卡'
}