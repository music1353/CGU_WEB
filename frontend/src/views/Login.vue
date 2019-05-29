<template>
<div @keyup.enter="login">
<v-app>
  <section id="login-section">
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm5 md5>
          <div class="login-block box-shadow">
            <v-container fluid fill-height pa-0>
              <!-- 右側登入欄 -->
              <v-flex md12>
                <!-- 登入表單部分 -->
                <v-layout column style="margin-left: 40px; margin-right: 40px;">
                  <div class="display-1 font-weight-medium" style="padding-bottom: 20px;">開始今天的遊戲
                    <a class="ranking-btn" href="javascript:void(0)" @click="rankDialog=true">
                      <i class="fas fa-trophy" style="font-size: 14px;"></i> 排行榜
                    </a>
                  </div>
                 
                  <v-flex md8>
                    <v-form ref="form" v-model="valid" lazy-validation>
                      <v-text-field v-model="account" :rules="accountRules" label="帳號" required></v-text-field>
                      <v-text-field v-model="pwd" :rules="passwordRules" label="密碼" required type="password"></v-text-field>
                    </v-form>
                  </v-flex>
                  <v-flex md4 class="mt-5">
                    <v-btn class="white--text" color="orange darken-1" :disabled="!valid" @click="login" :loading="loading">登入</v-btn>
                    <a class="forget-pass-btn" href="javascript:void(0)" @click="forgetPwd">忘記密碼?</a>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-container>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <!-- forget password dialog -->
    <v-dialog v-model="forgetPwdDialog" max-width="290">
      <v-card>
        <v-card-title class="headline">找回密碼</v-card-title>
        <v-container>
            <v-form ref="forgetPwdForm" v-model="forgetPwdFormValid" lazy-validation>
              <div v-if="getForgetPwdMsg==''">
                <v-text-field label="你的帳號" v-model="checkAccount" required :rules="checkAccountRules"></v-text-field>
                <v-text-field label="你的姓名" v-model="checkName" required :rules="checkNameRules"></v-text-field>
              </div>
              <div v-else>
                <p style="font-size: 20px;">{{ getForgetPwdMsg }}</p>
              </div>
            </v-form>
          
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat="flat" @click="forgetPwdDialog=false">取消</v-btn>
          <v-btn v-if="getForgetPwdMsg==''" color="green darken-1" flat="flat" @click="submit">送出</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- forget password dialog -->
    
    <!-- rank dialog start -->
    <v-dialog v-model="rankDialog" max-width="500">
      <v-tabs v-model="rankTabModel" dark centered color="orange darken-1" slider-color="orange darken-3" @change="changeTab" fixed-tabs>
        <v-tab v-for="item in rankModelList" :key="item">
          {{ item }}
        </v-tab>
      </v-tabs>
      <v-tabs-items>
        <v-tab-item>
          <v-card flat class="pa-4">
            <p style="font-size: 18px; text-align: center;">
              <i class="far fa-calendar-alt"></i>
              {{ week }}
            </p>
            <v-data-table :headers="headers" :items="rankData" class="elevation-1" hide-actions>
              <template slot="items" slot-scope="props">
                <td class="text-xs">{{ props.item.ranking }}
                  <i v-if="props.item.ranking==1" class="fas fa-crown" style="color: orange;"></i>
                </td>
                <td class="text-xs">{{ props.item.account }}</td>
                <td class="text-xs">{{ props.item.token }}</td>
              </template>
            </v-data-table>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-dialog>
    <!-- rank dialog end -->
  </section>
  <loading :parentToChild="loading" parentText="登入中..."></loading>
  <message :parentFlag="message" parentColor='EF5350' parentText='帳號或密碼錯誤！'></message>
  <nav-footer></nav-footer>
</v-app>
</div>
</template>

<script>
import axios from 'axios'

import NavFooter from "@/components/NavFooter.vue"
import Loading from "@/components/_partial/Loading.vue"
import Message from "@/components/_partial/Message.vue"

export default {
  components: {
    NavFooter,
    Loading,
    Message
  },
  data() {
    return {
      account: "",
      pwd: "",
      rePassCheckbox: false,
      // form valid
      valid: true,
      accountRules: [
        v => !!v || '您還沒有填寫帳號'
      ],
      passwordRules: [
        v => !!v || '您還沒有填寫密碼'
      ],
      // signup dialog
      dialog: false,
      // loading
      loading: false,
      // message
      message: false,
      // forgetPwdDialog
      forgetPwdDialog: false,
      forgetPwdFormValid: true,
      checkName: '',
      checkAccount: '',
      checkNameRules: [
        v => !!v || '您還沒有填寫姓名'
      ],
      checkAccountRules: [
        v => !!v || '您還沒有填寫帳號'
      ],
      getForgetPwdMsg: '',
      // rank dialog
      week: null,
      rankDialog: false,
      rankTabModel: null,
      rankModelList: ['實驗組', '對照組'],
      headers: [
        { text: '排名', align: 'left', sortable: false, value: 'ranking' },
        { text: '帳號', align: 'left', sortable: false, value: 'account' },
        { text: '星星數量', sortable: false, value: 'tokenNum' }
      ],
      rankData: []
    };
  },
  mounted() {
    this.checkLogin();
    this.getRank('userTest');
    this.getWeek();
  },
  methods: {
    login () {
      if (this.$refs.form.validate()) {
        this.loading = true;
        this.message = false;
        
        axios.post('/api/login', {
          account: this.account,
          pwd: this.pwd,
        }).then((response)=> {
          let res = response.data;
          if(res.status=='200') {
            if(res.result.authority=='admin')
              this.$router.push('/admin/index');
            else if(res.result.authority=='userTest' || res.result.authority=='userComp')
              this.$router.push('/user/index');
            else if(res.result.authority=='parentTest' || res.result.authority=='parentComp')
              this.$router.push('/parent/index');
          } else {
            this.loading = false;
            this.message = true;
          }
        });
      }
    },
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if(res.status=='200') {
          if(res.result.status == true) {
            if(res.result.authority == 'admin') {
              this.$router.push('/admin/index');
            } else if(res.result.authority=='userTest' || res.result.authority=='userComp') {
              this.$router.push('/user/index');
            } else if(res.result.authority == 'parentTest' || res.result.authority == 'parentComp') {
              this.$router.push('/parent/index');
            }
          }
        }
      });
    },
    forgetPwd() {
      this.checkName = '';
      this.checkAccount = '';
      this.getForgetPwdMsg = '';
      this.$refs.forgetPwdForm.resetValidation();
      this.forgetPwdDialog = true;
    },
    submit() {
      axios.get('/api/forgetPwd', {
        params: {
          'name': this.checkName,
          'account': this.checkAccount
        }
      }).then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.getForgetPwdMsg = '你的密碼是：'+res.result.pwd;
        } else {
          this.getForgetPwdMsg = res.msg;
        }
      });
    },
    getWeek() {
      axios.get('/api/rank/getWeek').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.week = res.result.week;
        }
      });
    },
    getRank(auth) {
      axios.get('/api/rank/getRank', {
        params: {
          authority: auth
        }
      }).then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let data = [];
          let count = 0;
          let prevToken = -10;
          res.result.forEach((element) => {
            if (element['token'] == prevToken) {
              element['ranking'] = count;
              data.push(element);
            } else {
              count++;
              element['ranking'] = count;
              data.push(element);
            }
            prevToken = element['token'];
          });

          this.rankData = data;
          // console.log(data);
        }
      });
    },
    changeTab() {
      if(this.rankTabModel == 0) {
        this.getRank('userTest');
      } else if (this.rankTabModel == 1) {
        this.getRank('userComp');
      }
    }
  } 
}
</script>

<style>
#login-section {
  height: 100vh;
  background-image: url('./../assets/image/bg6.jpg');
  background-size: cover;
  background-position:center bottom;
  /* background-size: contain;
  background-repeat: repeat; */
}

.login-block {
  display: block;
  height: 70vh;
}

.left-side {
  height: 100%;
  background-color: #FB8C00;
}

.signup-btn {
  text-decoration: none;
  color: #757575;
}

.signup-btn:hover {
  transition: all .2s;
  color: #FB8C00;
}

.forget-pass-btn {
  float: right;
  padding-top: 13px;
  text-decoration: none;
  color: #757575;
}

.ranking-btn {
  float: right; 
  font-size: 16px; 
  font-weight: 400; 
  padding-top: 6px;
  text-decoration: none;
  color: black;
  transition: ease all .3s;
}

.ranking-btn:hover {
  color: orange;
}

</style>
