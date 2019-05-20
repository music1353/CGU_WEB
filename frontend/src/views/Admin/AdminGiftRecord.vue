<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <div class="gift-title">
        <v-layout row align-center justify-start row wrap class="pa-2" style="font-size: 17px;">
          <v-flex lg2 md2 class="pl-4">
            <b>姓名</b>
          </v-flex>
          <v-flex lg2 md2 class="pl-4">
            <b>帳號</b>
          </v-flex>
          <v-flex lg2 md2>
            <b>禮物名稱</b>
          </v-flex>
          <v-flex lg2>
            <b>日期</b>
          </v-flex>
          <v-flex lg2 offset-lg2 class="pr-4">
            <b>操作</b>
          </v-flex>
        </v-layout>
      </div>
      <div v-for="item in giftExchangeRecords" :key="item.exchangeId">
        <v-hover>
          <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto">
            <v-layout row align-center justify-start row wrap class="pa-2" style="font-size: 17px;">
              <v-flex lg2 md2 class="pl-4">
                {{ item.userName }}
              </v-flex>
              <v-flex lg2 md2 class="pl-4">
                {{ item.userAccount }}
              </v-flex>
              <v-flex lg2 md2>
                {{ item.giftName }}
              </v-flex>
              <v-flex lg2>
                {{ item.date }}
              </v-flex>
              <v-flex lg2 offset-lg2 class="pr-4">
                <v-btn v-if="item.isGive==false" color="success" small class="mx-0" @click="sendGift(item.exchangeId)">送出禮物</v-btn>
                <v-icon class="mr-1 light-green--text py-2" v-if="item.isGive==true">done</v-icon>
                <span class="subheading light-green--text" v-if="item.isGive==true">done</span>
              </v-flex>
            </v-layout>
          </v-card>
        </v-hover>
      </div>
    </v-container>
  </v-content>
  <message :parentFlag="giftFlag" :parentColor='giftColor' :parentText='giftMsg'></message>
</v-app>
</div>
</template>
<script>
import axios from 'axios'
import NavHeaderAdmin from '@/components/NavHeaderAdmin'
import Message from "@/components/_partial/Message.vue"

export default {
  components: {
    NavHeaderAdmin,
    Message
  },
  data() {
    return {
      giftExchangeRecords: [],
      giftFlag: false,
      giftColor: '',
      giftMsg: '',
    }
  },
  mounted() {
    this.checkLogin();
    this.getGiftExchangeRecords();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.status == "200") {
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
    getGiftExchangeRecords() {
      axios.get('/api/gift/exchangeRecords').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.giftExchangeRecords = res.result;
        }
      });
    },
    sendGift(exchangeId) {
      this.giftFlag = false;

      axios.post('/api/gift/sendGift', {
        exchangeId: exchangeId
      }).then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.giftColor = '8BC34A';
          this.giftMsg = res.msg;
          this.giftFlag = true;
          
          this.getGiftExchangeRecords();
        }
      })
    }
  }
}
</script>