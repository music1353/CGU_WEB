<template>
<div>
<v-app>
  <nav-header-user></nav-header-user>
  <v-content>
    <v-container fluid grid-list-md grid-list-sm>
      <div style="font-size: 27px;" class="mb-4">
        <i class="fas fa-star award-icon"></i>
        你有 <span style="color: #FFC107; font-weight: bold;">{{tokenNum}}</span> 個星星
        <p style="font-size: 20px; color: #909399; margin-top:15px;">圖片為參考，數量不足時，實得之物品可能與附圖有異</p>
      </div>
      <!-- 禮品區 -->
      <v-layout align-center justify-start row fill-height wrap class="mb-4">
        <v-flex lg4 md6 v-for="item in giftList" :key="item.name" class="mb-3">
          <v-card>
            <v-img :src="item.imgURL" height="200px"></v-img>
            <v-card-actions class="mt-3 pb-4 mr-2 ml-2">
              <v-layout row wrap>
                <v-flex md10>
                  <span style="display: inline-block; font-size: 20px; height: 28px; line-height: 28px;">{{ item.name }}</span>
                  <v-icon style="display: inline-block; font-size:17px; line-height: 22px; margin-left: 5px;">star</v-icon>
                  <span v-if="userAuth=='userTest'" class="mr-2 ml-0" style="display: inline-block; font-size:17px; height: 28px; line-height: 28px;">{{ item.needToken*2 }}</span>
                  <span v-if="userAuth=='userComp'" class="mr-2 ml-0" style="display: inline-block; font-size:17px; height: 28px; line-height: 28px;">{{ item.needToken }}</span>
                </v-flex>
                <v-flex md2>
                  <a href="javascript:void(0)" id="exchange-btn" v-if="userAuth=='userTest'&&tokenNum>=item.needToken*2" @click="onConfirmExchangeDialog(item.name)">兌換</a>
                  <a href="javascript:void(0)" id="exchange-btn" v-if="userAuth=='userComp'&&tokenNum>=item.needToken" @click="onConfirmExchangeDialog(item.name)">兌換</a>
                </v-flex>
              </v-layout>
            </v-card-actions class="mt-4 mb-4 mr-2 ml-2">
          </v-card>
        </v-flex>
      </v-layout>
      <!-- 禮品區 -->
    </v-container>
    <message :parentFlag="giftFlag" :parentColor='giftColor' :parentText='giftMsg'></message>
    <nav-footer-simple></nav-footer-simple>

    <!-- confirm change dialog -->
    <v-dialog v-model="confirmExchangeDialog" max-width="290">
      <v-card>
        <v-card-title class="headline">兌換禮物</v-card-title>
        <v-card-text>確定是否要兌換 {{ giftName }} 呢?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" flat @click="confirmExchangeDialog=false">取消</v-btn>
          <v-btn color="green darken-1" flat @click="exchange">好</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- confirm change dialog -->
  </v-content>
</v-app>
</div>
</template>

<script>
import axios from 'axios'

import NavHeaderUser from '@/components/NavHeaderUser'
import NavFooterSimple from '@/components/NavFooterSimple'
import Message from "@/components/_partial/Message.vue"

export default {
  components: {
    NavHeaderUser,
    NavFooterSimple,
    Message
  },
  data() {
    return {
      userAuth: '', // 為了控制needToken顯示
      tokenNum: '',
      giftList: [],
      giftName: '',
      // message
      giftFlag: false,
      giftColor: '',
      giftMsg: '',
      // confirm change dialog
      confirmExchangeDialog: false
    }
  },
  mounted() {
    this.checkLogin();
    this.getTokenNum();
    this.getGiftList();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.result.status == true) {
          if (res.result.authority=='userTest' || res.result.authority=='userComp') {
            // pass
            this.userAuth = res.result.authority;
          } else if (res.result.authority == 'admin') {
            this.$router.push('/admin/index');
          } else if (res.result.authority=='parentTest' || res.result.authority=='parentComp') {
            this.$router.push('/parent/index');
          }
        } else {
          this.$router.push('/login');
        }
      });
    },
    getTokenNum() {
      axios.get('/api/token/getTokenNum').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.tokenNum = res.result.token;
        }
      });
    },
    getGiftList() {
      axios.get('/api/gift/getGifts').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.giftList = res.result;
        }
      });
    },
    onConfirmExchangeDialog(giftName) {
      this.confirmExchangeDialog = true;
      this.giftName = giftName;
    },
    exchange() {
      this.giftFlag = false;

      axios.post('/api/gift/exchange', {
        giftName: this.giftName
      }).then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.getTokenNum();
          this.getGiftList();

          this.confirmExchangeDialog = false;

          this.giftColor = '8BC34A';
          this.giftMsg = res.msg;
          this.giftFlag = true;
        }
      });
    }
  }
}
</script>

<style>
  #award-box {
    height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  #award-box .award-center {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 80%;
    text-align: center;
  }

  #award-box .award-center .award-icon{
    width: 100%;
    font-size: 100px;
    color: #FFC107;
  }

  #award-box .award-center .award-text {
    line-height: 130px;
    font-size: 35px;
  }

  #exchange-btn {
    display: inline-block;
    color: #fb8c00;
    display: inline-block; 
    font-size:17px; 
    height: 28px; 
    line-height: 28px;
    text-decoration: none;
  }
  
</style>
