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
                  <div class="display-1 font-weight-medium" style="padding-bottom: 20px;">開始今天的遊戲</div>
                  <v-flex md8>
                    <v-form ref="form" v-model="valid" lazy-validation>
                      <v-text-field v-model="account" :rules="accountRules" label="帳號" required></v-text-field>
                      <v-text-field v-model="pwd" :rules="passswordRules" label="密碼" required type="password"></v-text-field>
                      <v-checkbox v-model="rePassCheckbox" label="記住密碼" required ></v-checkbox>
                    </v-form>
                  </v-flex>
                  <v-flex md4 style="padding-top: 10px;">
                    <v-btn class="white--text" color="orange darken-1" :disabled="!valid" @click="login" :loading="loading">登入</v-btn>
                    <a class="signup-btn" style="cursor: pointer;" @click="dialog=true">註冊</a>
                    <a class="forget-pass-btn" href="">忘記密碼?</a>
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-container>
          </div>
          
        </v-flex>
      </v-layout>
    </v-container>
  </section>

  <!-- 註冊 dialog start -->
  <v-layout row justify-center>
    <v-dialog v-model="dialog"  max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">註冊</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 md4>
                <v-text-field label="姓名" required></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field label="Legal middle name" hint="example of helper text only on focus"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field label="Legal last name*" hint="example of persistent helper text" persistent-hint required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Email*" required></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field label="Password*" type="password" required></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-select :items="['0-17', '18-29', '30-54', '54+']" label="年齡*" required style="top: 0px;"></v-select>
              </v-flex>
              <v-flex xs12 sm6>
                <v-autocomplete :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']" label="Interests" multiple></v-autocomplete>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="dialog = false">Close</v-btn>
          <v-btn color="blue darken-1" flat @click="dialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
  <!-- 註冊 dialog end -->
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
      passswordRules: [
        v => !!v || '您還沒有填寫密碼'
      ],
      // signup dialog
      dialog: false,
      // loading
      loading: false,
      // message
      message: false
    };
  },
  mounted() {
    this.checkLogin();
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
          if(res.result.status==true) {
            if(res.result.authority == 'admin') {
              this.$router.push('/admin/index');
            } else if(res.result.authority=='userTest' || res.result.authority=='userComp') {
              this.$router.push('/user/index');
            } else if(res.result.authority == 'parent') {
              this.$router.push('/parent/index');
            }
          }
        }
      });
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

</style>
