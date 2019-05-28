<template>
<div>
<v-app>
  <nav-header-parent></nav-header-parent>
  <v-content>
    <v-container>
      <v-card>
        <!-- 孩子個遊戲的level start -->
        <v-card-title class="headline font-weight-medium blue-grey white--text">孩子各個訓練任務的level</v-card-title>
        <v-container>
          <v-layout align-center justify-start row wrap>
            <v-flex layout md3 v-for="game in childLevel" class="px-3 mb-3" :key="game.gameNameEN">
              <v-hover>
                <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
                  <v-card-title>
                    <div>
                      <span class="headline"> {{game.gameNameCH}} </span>
                      <div class="d-flex">
                        <div class="ml-2 grey--text text--darken-2">
                          <span>({{ game.level }})</span>
                        </div>
                      </div>
                    </div>
                    <v-spacer></v-spacer>
                    <v-btn icon class="mr-0" @click="showIntro(game.gameNameEN, game.gameNameCH)">
                      介紹
                    </v-btn>
                  </v-card-title>
                </v-card>
              </v-hover>
            </v-flex>
          </v-layout>
        </v-container>
        <!-- 孩子個遊戲的level end -->
        <!-- 孩子今天的訓練任務 start -->
        <v-card-title class="headline font-weight-medium blue-grey white--text">孩子今天的訓練任務</v-card-title>
        <v-container>
          <v-layout align-center justify-start row wrap class="mt-3">
            <v-flex layout xs12 md4 v-for="card in childGames" :key="card.title" class="px-3 mb-3">
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
                    <v-btn icon class="mr-0" @click="showIntro(card.gameNameEN, card.gameNameCH)">
                      介紹
                    </v-btn>
                  </v-card-title>
                </v-card>
              </v-hover>
            </v-flex>
          </v-layout>
          <p style="font-size: 17px;" v-if="childGames.length==0">今天沒有訓練任務！</p>
        </v-container>
        <!-- 孩子今天的遊戲任務 end -->

        <v-card-title class="headline font-weight-medium blue-grey white--text">請協助評估孩子今天的訓練情形</v-card-title>
        <v-container>
          <v-subheader class="pa-0 title">1. 在注意力方面</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md1><span class="grey--text text--darken-3">很不專心</span></v-flex>
              <v-flex md10 class="pr-0">
                <v-slider v-model="focusValue" thumb-label="always" style="width:100%" :disabled="!canDo"></v-slider>
              </v-flex>
              <v-flex md1><span class="grey--text text--darken-3">很專心</span></v-flex>
              <v-flex shrink style="width: 60px">
                <v-text-field v-model="focusValue" class="mt-0" hide-details single-line type="number" :disabled="!canDo"></v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="pt-0">
          <v-subheader class="pa-0 title">2. 在情緒穩定度方面</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md1><span class="grey--text text--darken-3">很不穩定</span></v-flex>
              <v-flex md10 class="pr-0">
                <v-slider v-model="emotionValue" thumb-label="always" style="width:100%" :disabled="!canDo"></v-slider>
              </v-flex>
              <v-flex md1><span class="grey--text text--darken-3">很穩定</span></v-flex>
              <v-flex shrink style="width: 60px">
                <v-text-field v-model="emotionValue" class="mt-0" hide-details single-line type="number" :disabled="!canDo"></v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="pt-0">
          <v-subheader class="pa-0 title">3. 在訓練動機上</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md1><span class="grey--text text--darken-3">很沒有動機</span></v-flex>
              <v-flex md10 class="pr-0">
                <v-slider v-model="motivationValue" thumb-label="always" style="width:100%" :disabled="!canDo"></v-slider>
              </v-flex>
              <v-flex md1><span class="grey--text text--darken-3">很有動機</span></v-flex>
              <v-flex shrink style="width: 60px">
                <v-text-field v-model="motivationValue" class="mt-0" hide-details single-line type="number" :disabled="!canDo"></v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="py-0">
          <v-subheader class="pa-0 title">4. 有無回饋的訊息</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md12>
                <v-textarea box name="input-7-4" label="感謝您提供寶貴的建議與回饋" v-model="feedback" :disabled="!canDo"></v-textarea>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="pt-0 mt-0">
          <v-layout row>
            <v-flex md12 v-if="canDo">
              <v-btn :loading="loading" :disabled="loading" color="blue-grey" class="white--text" @click="submit" style="float: right;">完成</v-btn>
            </v-flex>
          </v-layout>
        </v-container>   
      </v-card>
    </v-container>
  </v-content>

  <v-dialog v-model="gameIntroDialog" width="500">
    <v-card>
      <v-card-title class="headline grey lighten-2" primary-title>{{ gameIntroTitle }}</v-card-title>
      <v-card-text style="font-size: 20px;">{{ gameIntroContent }}</v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" flat @click="gameIntroDialog=false">了解</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <message :parentFlag="completeMessage" parentColor='8BC34A' parentText='您的回饋已經確實收到！'></message>
  <message :parentFlag="errorMessage" parentColor='EF5350' parentText='發送錯誤！'></message>
</v-app>
</div>
</template>

<script>
import NavHeaderParent from '@/components/NavHeaderParent'
import Message from '@/components/_partial/Message.vue'
import { gameIntro } from '@/utils/GameIntro.js'

export default {
  components: {
    NavHeaderParent,
    Message
  },
  data() {
    return {
      focusValue: 0, // 1.專注力
      emotionValue: 0, // 2.情緒穩定度
      motivationValue: 0, // 3.訓練動機
      feedback: '', //4.回饋
      loading: false,
      // message
      completeMessage: false,
      errorMessage: false,
      canDo: true,
      // child games card
      childGames: [],
      childLevel: [],
      gameIntroDialog: false,
      gameIntroTitle: '',
      gameIntroContent: ''
    }
  },
  mounted() {
    this.checkLogin();
    this.checkDailyPSQ();
    this.getChildGames();
    this.getChildLevel();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.status == "200") {
          if (res.result.authority=='userTest' || res.result.authority=='compTest') {
            this.$router.push('/user/index');
          } else if (res.result.authority == 'admin') {
            this.$router.push('/admin/index')
          } else if (res.result.authority=='parentTest' || res.result.authority=='parentComp') {
            // pass
          }
        } else {
          this.$router.push('/login');
        }
      });
    },
    checkDailyPSQ() {
      axios.get('/api/parent/checkDailyPSQ').then((response)=> {
        let res = response.data;
        if(res.status=='200') {
          if(res.result.canDo==true) {
            this.canDo = true;
          } else {
            this.canDo = false;
            this.focusValue = parseInt(res.result.focusValue);
            this.emotionValue = parseInt(res.result.emotionValue);
            this.motivationValue = parseInt(res.result.motivationValue);
            this.feedback = res.result.feedback;
          }
        }
      })
    },
    getChildGames() {
      axios.get('/api/parent/getChildGames').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          if(res.msg == true) {
            this.childGames = res.result;
          } else {
            console.log('今天沒有訓練任務');
          }
        }
      });
    },
    getChildLevel() {
      axios.get('/api/parent/getChildLevel').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let levelList = res.result

          // 如果是今天的遊戲就highlight
          let todayGameList = [];
          this.childGames.forEach((element) => {
            todayGameList.push(element['gameNameEN']);
          });
          levelList.forEach((element, index) => {
            if( todayGameList.includes(element['gameNameEN']) ) {
              levelList[index]['highlight'] = true; 
            }
          });

          this.childLevel = levelList;
        }
      });
    },
    showIntro(gameNameEN, gameNameCH) {
      this.gameIntroTitle = gameNameCH;
      this.gameIntroContent = gameIntro[gameNameEN];
      this.gameIntroDialog = true;
    },
    submit() {
      this.loading = true;

      axios.post('/api/parent/sendPSQ', {
        focusValue: this.focusValue.toString(),
        emotionValue: this.emotionValue.toString(),
        motivationValue: this.motivationValue.toString(),
        feedback: this.feedback
      }).then((response)=> {
        let res = response.data;
        if(res.status=='200') {
          this.completeMessage = true;
          this.loading = false;
          this.checkDailyPSQ();
        } else {
          this.loading = false;
          this.errorMessage = false;
        }
      });
    }
  }
}
</script>