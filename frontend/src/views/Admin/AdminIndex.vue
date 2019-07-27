<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <v-card>
        <v-container fluid id="today-pratice-status-section">
          <p class="display-1">今日練習狀況</p>
          <v-divider class="my-3"></v-divider>
          <!-- test group panel start -->
          <div class="test-group panel">
            <!-- <div class="panel-title">實驗組</div> -->
            <v-chip color="primary" text-color="white" style="font-size: 16px;">實驗組</v-chip>
            <div class="panel-cards">
              <v-layout align-center justify-start row fill-height wrap>
                <v-flex layout lg2 md3 v-for="item in testGroupData" :key="item.account" style="margin: 7px;">
                  <v-hover>
                    <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
                      <v-card-title primary-title>
                        <div>
                          <div class="headline">{{ item.name }}</div>
                          <span class="grey--text">{{ item.account }}</span>
                        </div>
                      </v-card-title>
                      <v-card-actions>
                        <v-layout align-center justify-end style="height: 30px;">
                            <v-icon class="mr-1 light-green--text" v-if="item.complete==true">done</v-icon>
                            <v-icon class="mr-1" v-else>clear</v-icon>
                            <span class="subheading light-green--text" v-if="item.complete==true">done</span>
                            <span class="subheading grey--text" v-else>incomplete</span>
                          </v-layout>
                      </v-card-actions>
                    </v-card>
                  </v-hover>
                </v-flex>
              </v-layout>
            </div>
          </div>
          <!-- test group panel end -->
          <!-- comparison group panel start -->
          <div class="comparison-group panel">
            <!-- <div class="panel-title">對照組</div> -->
            <v-chip color="green" text-color="white" style="font-size: 16px;">對照組</v-chip>
            <div class="panel-cards">
              <v-layout align-center justify-start row fill-height wrap>
                <v-flex layout lg2 md3 v-for="item in compGroupData" :key="item.account" style="margin: 7px;">
                  <v-hover>
                    <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
                      <v-card-title primary-title>
                        <div>
                          <div class="headline">{{ item.name }}</div>
                          <span class="grey--text">{{ item.account }}</span>
                        </div>
                      </v-card-title>
                      <v-card-actions>
                        <v-layout align-center justify-end style="height: 30px;">
                          <v-icon class="mr-1 light-green--text" v-if="item.complete==true">done</v-icon>
                          <v-icon class="mr-1" v-else>clear</v-icon>
                          <span class="subheading light-green--text" v-if="item.complete==true">done</span>
                          <span class="subheading grey--text" v-else>incomplete</span>
                        </v-layout>
                      </v-card-actions>
                    </v-card>
                  </v-hover>
                </v-flex>
              </v-layout>
            </div>
          </div>
          <!-- comparison group panel end -->
        </v-container>
      </v-card>

      <!-- TODO: -->
      <v-card style="margin-top: 20px;">
        <v-container fluid id="week-pratice-status-section">
          <p class="display-1">
            每週練習狀況
            <span style="font-size: 20px;">(只呈現
              <span style="color:#F57C00;">完成任務</span>
              及
              <span style="color:#F57C00;">完成遊戲</span>
              的名單)
            </span>
          </p>
          <v-divider class="my-3"></v-divider>
          <v-layout row>
            <v-flex md3 xs12>
              <v-select @change="changeWeek" v-model="weekSelect" :items="weekItems" label="Solo field" solo></v-select>
            </v-flex>
            <v-flex md3 xs12>
              <p style="margin-top: 22px; font-size: 16px;">&nbsp; (現在是 <b>{{nowWeekCH}}</b>)</p>
            </v-flex>
          </v-layout>
          <v-layout row style="height: 400px;">
            <v-flex md6 style="border-right: 1px #E4E7Ed dashed; overflow-y: scroll;">
              <v-chip color="primary" text-color="white" style="font-size: 16px;">實驗組</v-chip>
              <div v-for="user in userTestList" style="margin-top: 10px; margin-left:15px; font-size: 20px;">
                <v-icon style="font-size: 25px;">mdi-account</v-icon> {{user.name}}
                <span class="subheading grey--text">{{user.account}}</span>
              </div>
            </v-flex>
            <v-flex md6 style="margin-left: 10px;">
              <v-chip color="green" text-color="white" style="font-size: 16px;">對照組</v-chip>
              <div v-for="user in userCompList" style="margin-top: 10px; margin-left:15px; font-size: 20px;">
                <v-icon style="font-size: 25px;">mdi-account</v-icon> {{user.name}}
                <span class="subheading grey--text">{{user.account}}</span>
              </div>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-container fluid>
  </v-content>
</v-app>
</div>
</template>

<script>
import axios from 'axios'
import NavHeaderAdmin from '@/components/NavHeaderAdmin'
var date = new Date();

export default {
  components: {
    NavHeaderAdmin
  },
  data() {
    return {
      // today
      'date': new Date().toISOString().substr(0, 10),
      'testGroupData': [],
      'compGroupData': [],
      // week
      nowWeek: 1, // 現在第幾週(數字)
      nowWeekCH: '', // 現在第幾週(中文)
      weekItems: ['第一週', '第二週', '第三週', '第四週', '第五週', '第六週', '第七週'],
      weekSelect: '第一週',
      userTestList: [], // 測試組：選定週完成登入任務及全部完成任務的名單
      userCompList: [] // 對照組
    }
  },
  mounted() {
    this.checkLogin();
    this.getDailyUsersInfo();
    this.getWeek();
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
    getDailyUsersInfo() {
      axios.get('/api/admin/getDailyUsersInfo').then((response)=> {
        let res = response.data;
        if (res.status == "200") {
          res.result.forEach((element)=> {
            if(element['authority']=='userTest') {
              this.testGroupData.push(element);
            } else if(element['authority']=='userComp') {
              this.compGroupData.push(element);
            }
          });
        }
      });
    },
    getWeek() {
      axios.get('/api/rank/getWeek').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.nowWeekCH = res.result.week;
          if (res.result.week == '第一週') this.nowWeek = 1;
          else if (res.result.week == '第二週') this.nowWeek = 2;
          else if (res.result.week == '第三週') this.nowWeek = 3;
          else if (res.result.week == '第四週') this.nowWeek = 4;
          else if (res.result.week == '第五週') this.nowWeek = 5;
          else if (res.result.week == '第六週') this.nowWeek = 6;
          else if (res.result.week == '第七週') this.nowWeek = 7;
          else if (res.result.week == '第八週') this.nowWeek = 8;
          else if (res.result.week == '第九週') this.nowWeek = 9;
          else if (res.result.week == '第十週') this.nowWeek = 10;

          this.getDoneMissionUser(this.nowWeek);
        }
      });
    },
    getDoneMissionUser(week) {
      axios.get('/api/admin/doneMissionUser', {
        params: {
          week: week
        }
      }).then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.userTestList = res.result.userTestList;
          this.userCompList = res.result.userCompList;
        }
      });
    },
    changeWeek() {
      let reqWeek = 1;
      if (this.weekSelect == '第一週') reqWeek = 1;
      else if (this.weekSelect == '第二週') reqWeek = 2;
      else if (this.weekSelect == '第三週') reqWeek = 3;
      else if (this.weekSelect == '第四週') reqWeek = 4;
      else if (this.weekSelect == '第五週') reqWeek = 5;
      else if (this.weekSelect == '第六週') reqWeek = 6;
      else if (this.weekSelect == '第七週') reqWeek = 7;
      else if (this.weekSelect == '第八週') reqWeek = 8;
      else if (this.weekSelect == '第九週') reqWeek = 9;
      else if (this.weekSelect == '第十週') reqWeek = 10;

      this.getDoneMissionUser(reqWeek);
    }
  }
}
</script>

<style>
  #daily-done-panel .date-title-block .date-title {
    color: rgb(29, 29, 155);
    font-size: 30px;
    font-weight: bold;
  }

  .panel .panel-title {
    font-size: 30px;
    font-weight: bold;
  }
  .panel .panel-cards {
    margin-top: 10px;
    margin-bottom: 30px;
  }
</style>
