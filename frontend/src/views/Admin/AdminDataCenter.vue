<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <v-card>
        <v-container fluid>
          <div class="user-data mb-3">
            <p class="headline">使用者資料</p>
            <!-- <v-icon large color="green darken-2" class="mr-3" style="font-size: 25px;">fas fa-file-csv</v-icon> -->
            <v-btn color="#01579B" class="white--text ml-0" large @click="getUserData">
              使用者資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
            <v-btn color="#01579B" class="white--text ml-0" large @click="getParentData">
              家長資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
            <v-btn color="#01579B" class="white--text ml-0" large @click="getAdminData">
              管理員資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
          <v-divider></v-divider>
          <div class="game-data mt-3 mb-3">
            <p class="headline">遊戲資料</p>
            <v-btn color="#558B2F" class="white--text ml-0" large @click="getGameData">
              遊戲紀錄資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
          <v-divider></v-divider>
          <div class="game-data mt-3 mb-3">
            <p class="headline">問卷資料</p>
            <v-btn color="blue-grey" class="white--text ml-0" large @click="getQuestionnairesData">
              問卷資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
          <v-divider></v-divider>
          <div class="game-data mt-3 mb-3">
            <p class="headline">禮物兌換資料</p>
            <v-btn color="red darken-2" class="white--text ml-0" large @click="getGiftExchangeData">
              禮物兌換資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
        </v-container>
      </v-card>
    </v-container>
  </v-content>
</v-app>
</div>
</template>
<script>
import axios from 'axios'
// import * as jsonexport from "jsonexport/dist"
import { json2csv } from '@/utils/json2csv.js'
import NavHeaderAdmin from '@/components/NavHeaderAdmin'

export default {
  components: {
    NavHeaderAdmin
  },
  data() {
    return {
      
    }
  },
  mounted() {
    this.checkLogin();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.result.status == true) {
          if (res.result.authority=='userTest' || res.result.authority=='compTest') {
            this.$router.push('/user/index');
          } else if (res.result.authority == 'admin') {
            // pass
          } else if (res.result.authority=='parentTest' || res.result.authority=='parentComp') {
            this.$router.push('/parent/index')
          }
        } else {
          this.$router.push('/login');
        }
      });
    },
    getUserData() {
      axios.get('/api/data/user').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;

          let options = {
            headers: ['authority', 'account', 'pwd', 'name', 'token', 'parentAccount', 'parentPwd', 'parentName', 'phone'],
            rename: ['身份', '帳號', '密碼', '姓名', '星星數', '家長帳號', '家長密碼', '家長姓名', '聯絡電話']
          }
          json2csv(result, '使用者資料', options);
        }
      });
    },
    getParentData() {
      axios.get('/api/data/parent').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;

          let options = {
            headers: ['authority', 'account', 'pwd', 'name', 'phone'],
            rename: ['身份', '帳號', '密碼', '姓名', '聯絡電話']
          }
          json2csv(result, '家長資料', options);
        }
      });
    },
    getAdminData() {
      axios.get('/api/data/admin').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;

          let options = {
            headers: ['authority', 'account', 'pwd', 'name'],
            rename: ['身份', '帳號', '密碼', '姓名']
          }
          json2csv(result, '管理員資料', options);
        }
      });
    },
    getGameData() {
      axios.get('/api/data/game').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;

          let options = {
            rename: ['帳號', '日期', '遊戲中文名稱', '遊戲英文名稱', 'level', '反應時間', '正確率', '正確次數']
          }
          json2csv(result, '遊戲紀錄資料', options);
        }
      });
    },
    getQuestionnairesData() {
      axios.get('/api/data/questionnaires').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;

          let options = {
            headers: ['authority', 'account', 'name', 'parentAccount', 'parentName', 'questionnaires.date', 'questionnaires.focusValue', 'questionnaires.emotionValue', 'questionnaires.motivationValue', 'questionnaires.feedback'],
            rename: ['身份', '帳號', '姓名', '家長帳號', '家長姓名', '日期', '注意力', '情緒穩定度', '訓練動機', '回饋']
          }
          json2csv(result, '問卷資料', options);
        }
      });
    },
    getGiftExchangeData() {
      axios.get('/api/data/giftExchange').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;

          let options = {
            headers: ['date', 'account', 'name', 'giftName', 'isGive'],
            rename: ['帳號', '姓名', '禮物名稱', '兌換日期', '是否寄出']
          }
          json2csv(result, '禮物兌換資料', options);
        }
      });
    }
  }
}
</script>