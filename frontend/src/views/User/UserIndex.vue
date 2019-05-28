<template>
<div>
<v-app>
  <nav-header-user></nav-header-user>
  <v-content >
    <v-container fluid grid-list-md grid-list-sm>
      <v-alert :value="todayIsComplete" type="success" transition="scale-transition">
        今天的遊戲都已經完成了！
      </v-alert>
      <v-layout v-if="doFlag" align-center justify-start row wrap class="mt-3">
        <v-flex layout xs12 md4 v-for="card in gamesCards" :key="card.title" class="px-3 mb-3">
          <v-hover>
            <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
              <v-img :aspect-ratio="16/9" :src="card.imgURL"></v-img>
              <v-card-title>
                <div>
                  <span class="headline"> {{card.gameNameCH}} </span>
                  <div class="d-flex">
                    <div class="ml-2 grey--text text--darken-2">
                      <span>({{ card.level }})</span>
                    </div>
                  </div>
                </div>
                <v-spacer></v-spacer>
                <v-btn icon class="mr-0" :to="card.link" :disabled='card.complete'>
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-card-title>
            </v-card>
          </v-hover>
        </v-flex>
      </v-layout>
      <v-layout v-else>
        <v-jumbotron :gradient="gradient" dark src="https://cdn.vuetifyjs.com/images/parallax/material2.jpg" style="width: 100vw; height: 80vh;">
          <v-container fill-height>
            <v-layout align-center>
              <v-flex text-xs-center>
                <h3 class="display-3">今天沒有遊戲</h3>
                <div class="title mt-5">下次記得來玩呦！</div>
              </v-flex>
            </v-layout>
          </v-container>
        </v-jumbotron>
      </v-layout>
    </v-container>
    <nav-footer-simple></nav-footer-simple>
  </v-content>
  <message :parentFlag="msgFlag" parentColor='FFB300' :parentText='msgCxt'></message>
</v-app>
</div>
</template>

<script>
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
      doFlag: true, // 今天有沒有遊戲玩
      todayIsComplete: false, // 今天所有遊戲是否都完成
      gamesCards: [],
      gradient: 'to top right, rgba(63,81,181, .7), rgba(25,32,72, .7)',
      msgFlag: false,
      msgCxt: ''
    }
  },
  mounted() {
    this.checkLogin();
    this.getGames();
    this.checkLoginMission();
    this.checkPlayMission();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.status == "200") {
          if (res.result.authority=='userTest' || res.result.authority=='userComp') {
            // pass
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
    getGames() {
      axios.get('/api/user/getGames').then((response) => {
        let res = response.data;
        this.doFlag = res.msg;
        if (res.status == '200') {
          this.gamesCards = res.result;
          // console.log(this.gamesCards);
          this.getAllGameIsComplete();
        }
      });
    },
    getAllGameIsComplete() {
      axios.get('/api/user/getAllGameIsComplete').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.todayIsComplete = res.result.complete;
          
          // 把每個遊戲的complete狀態加進card
          this.gamesCards.forEach((element) => {
            element['complete'] = res.result[element.gameNameEN];
          });
        }
      });
    },
    checkLoginMission() {
      this.msgFlag = false;

      axios.post('/api/token/loginMission').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.msgCxt = '完成每日登入任務 +50星星'
          this.msgFlag = true;
        }
      });
    },
    checkPlayMission() {
      this.msgFlag = false;

      axios.post('/api/token/playMission').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          if (res.result.addTokenNum > 0) {
            this.msgCxt = '完成一項遊戲 +10星星'
            this.msgFlag = true;
          }
        }
      });
    }
  }
}
</script>