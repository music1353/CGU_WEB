# Training ADHD children Website

This project is cooperating with the department of occupational therapy of Chang Gung University

A website for training ADHD children based on Vue and Flask

Training game is based on Unity

[![Vue](https://img.shields.io/badge/vue-2.5.2-blue.svg)](https://github.com/vuejs/vue) ![vuetify](https://img.shields.io/badge/vuetify-1.3.8-blue.svg) ![flask](https://img.shields.io/badge/flask-1.0.3-blue.svg)



## Feactures

* There are seven training games：
  1. 正序寵物樂園（視覺空間記憶）
  2. 逆序寵物樂園
  3. 正序動物農莊（聲音專注）
  4. 逆序動物農莊
  5. 老師點點名（對照文字）
  6. 橡果去哪兒（思維、觀察）
  7. 球球滿天飛（反應力）
* According to different identities（實驗組、對照組）, updated daily training games
* Admin can monitor the daily training progress of each trainer
* The trainer's parents can follow the training progress and fill out feedback forms to participate in the training process
* It's a smooth experience on different devices, including phones, tablets, and computers



## Implementation

**Environment**：

- Windows 10
- Node 11.2.0
- Yarn 1.16.0
- Vue 2.5.2
- Flask 1.0.3

**Server**：Nginx 1.16.0

**Database**：MongoDB 3.6.12



## Get Started

~~~bash
# build frontend
yarn run build

# run nginx
start nginx

# run backend
python server.py

# run mongodb
mongod
~~~



## Screenshots

* Login Index

  ![Imgur](https://i.imgur.com/MfsSXYu.png)

* User

  ![Imgur](https://i.imgur.com/6ZhHc9F.png)

  ![Imgur](https://i.imgur.com/pV4x14b.png)

* Admin

  ![Imgur](https://i.imgur.com/x0luWgB.png)

  ![Imgur](https://i.imgur.com/Njb8bMW.png)

* Parent

  ![Imgur](https://i.imgur.com/8yVRElp.png)

  ![Imgur](https://i.imgur.com/mVC6OrM.png)



## License

長庚大學職能治療系 © 2018, Chin-Hsuan Su