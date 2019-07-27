<template>
<div>
  <v-navigation-drawer :clipped="clipped" v-model="drawer" enable-resize-watcher app dark class="lighten-3">
    <v-list>
      <!-- v-link-group => div -->
      <div v-for="item in items" :value="item.icon" :key="item.title">
        <v-list-tile :to="item.linkto" active-class="grey darken-4">
          <v-list-tile-action>
              <v-icon> {{item.icon}} </v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title> {{item.title}}</v-list-tile-title>
          </v-list-tile-content> 
        </v-list-tile>
      </div>
    </v-list>
  </v-navigation-drawer> 
  <v-toolbar fixed app :clipped-left="clipped" dark color="grey darken-3">
    <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
    <v-toolbar-title class="white--text"><a href="/admin/index" class="white--text" style="text-decoration: none;">管理員後台</a></v-toolbar-title>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
      <v-btn icon @click="rankDialog=true">
        <v-tooltip bottom>
          <v-icon slot="activator" style="font-size: 18px;">fas fa-trophy</v-icon>
          <span>排名</span>
        </v-tooltip>
      </v-btn>
      <v-btn flat class="title">{{name}}</v-btn>
      <v-btn color="orange darken-2" @click="logout">
        登出<v-icon dark right>logout</v-icon>
      </v-btn>
  </v-toolbar>

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
</div>
</template>

<script>
import axios from 'axios'

export default {
  components: {},
  data() {
    return {
      account: '',
      name: '',
      authority: '',
      drawer: true,
      clipped: true,
      // items
      items: [{
        'icon': 'fas fa-dice-d6',
        'title': '練習狀況',
        'linkto': 'index',
      }, {
        'icon': 'fas fa-user-edit',
        'title': '使用者管理',
        'linkto': 'usersManage'
      }, {
        'icon': 'fas fa-gift',
        'title': '兌換紀錄',
        'linkto': 'giftRecord'
      }, {
        'icon': 'border_color',
        'title': '意見回饋',
        'linkto': 'feedback'
      }, {
        'icon': 'fas fa-database',
        'title': '資料中心',
        'linkto': 'dataCenter'
      }],
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
    }
  },
  mounted() {
    this.getUserInfo();
    this.getRank('userTest');
    this.getWeek();
  },
  methods: {
    logout() {
      axios.post('/api/logout').then((response)=> {
        let res = response.data;
        if (res.status == '200') {
          this.$router.push('/login');
        }
      });
    },
    getUserInfo() {
      axios.get('/api/getUserInfo').then((response)=>{
        let res = response.data;
        if (res.status == '200') {
          this.account = res.result.account;
          this.name = res.result.name;
          this.authority = res.result.authority;
        }
      })
    },
    // rank
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