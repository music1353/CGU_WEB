<template>
<div>
  <v-navigation-drawer :clipped="clipped" v-model="drawer" enable-resize-watcher app dark class="lighten-3">
    <v-list>
      <div v-for="item in items" :value="item.icon" :key="item.title">
        <v-list-tile :to="item.linkto" active-class="grey darken-4">
          <v-list-tile-action>
              <v-icon> {{item.icon}} </v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{item.title}}</v-list-tile-title>
          </v-list-tile-content> 
        </v-list-tile>
      </div>
    </v-list>
  </v-navigation-drawer> 
  <v-toolbar fixed app :clipped-left="clipped" dark color="grey darken-3">
    <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
    <v-toolbar-title class="white--text"><a href="/user/index" class="white--text" style="text-decoration: none;">長庚大學</a></v-toolbar-title>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
      <v-btn icon @click="rankDialog=true">
        <v-tooltip bottom>
          <v-icon slot="activator" style="font-size: 18px;">fas fa-trophy</v-icon>
          <span>排名</span>
        </v-tooltip>
      </v-btn>
      <v-btn icon @click="missionDialog=true">
        <v-tooltip bottom>
          <v-icon slot="activator" style="font-size: 18px;">fas fa-scroll</v-icon>
          <!-- TODO: mission card -->
          <v-card flat class="pa-4" id="mission-card">
            <p class="title" style="margin-bottom: 25px;">每日任務進度</p>
            <p style="font-size:14px; color:">
              <v-icon style="font-size:18px; margin-left:4px;">{{loginIcon}}</v-icon>
              <span style="font-size:16px; margin-left:9px;">登入任務 (+50)</span>
            </p>
            <p style="font-size:14px; color:">
              <span style="">{{missionData.completeGameTimes}}/3</span>
              <span style="font-size:16px; margin-left:8px;">完成遊戲次數 (+10)</span>
            </p>
            <p style="font-size:14px; color:">
              <v-icon style="font-size:18px; margin-left:4px;">{{allCompleteIcon}}</v-icon>
              <span style="font-size:16px; margin-left:9px;">所有遊戲都完成 (+20)</span>
            </p>
            <p style="font-size:14px;">
              <span style="color:white;">{{missionData.levelUpTimesMission}}/6</span>
              <span style="font-size:16px; margin-left:8px; color:white;">遊戲升級次數 (+20)</span>
            </p>
          </v-card>
        </v-tooltip>
      </v-btn>
      <v-btn flat class="title">{{name}}</v-btn>
      <v-btn color="orange darken-2" @click="logout">
        登出<v-icon dark right>logout</v-icon>
      </v-btn>
  </v-toolbar>

  <!-- rank dialog start -->
  <v-dialog v-model="rankDialog" max-width="500">
    <v-card flat class="pa-4">
      <p style="font-size: 18px; text-align: center;">
        <i class="far fa-calendar-alt"></i>
        {{ week }} - {{ authCHIN }}
      </p>
      <v-data-table id="rank-table" :headers="headers" :items="rankData" class="elevation-1" hide-actions>
        <template slot="items" slot-scope="props">
          <td class="text-xs">{{ props.item.ranking }}
            <i v-if="props.item.ranking==1" class="fas fa-crown" style="color: orange;"></i>
          </td>
          <td class="text-xs">{{ props.item.account }}</td>
          <td class="text-xs">{{ props.item.token }}</td>
        </template>
      </v-data-table>
    </v-card>
  </v-dialog>
  <!-- rank dialog end -->

  <!-- TODO: mission dialog start -->
  <!-- <v-dialog v-model="missionDialog" max-width="500">
    <v-card flat class="pa-4">
      <p class="title">每日任務進度</p>
      <v-checkbox style="color: black !important;" disabled v-model="missionData.login" label="每日登入任務"></v-checkbox>
      <p style="font-size:14px;">
        <span style="color:#1565C0;">{{missionData.playMission}}/3</span>
        <span style="font-size:16px; margin-left:8px; color: black;">完成遊戲次數</span>
      </p>
      <v-checkbox disabled v-model="missionData.allComplete" label="所有遊戲都完成"></v-checkbox>
      <p style="font-size:14px;">
        <span style="color:#1565C0;">{{missionData.levelUpTimes}}/6</span>
        <span style="font-size:16px; margin-left:8px; color: black;">遊戲升級次數</span>
      </p>
    </v-card>
  </v-dialog> -->
  <!-- mission dialog end -->
</div>
</template>

<script>
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
        'title': '遊戲面板',
        'linkto': 'index',
      }, {
        'icon': 'fas fa-gift',
        'title': '兌換禮物',
        'linkto': 'award'
      }],
      // rank dialog
      week: null,
      authCHIN: '',
      rankDialog: false,
      headers: [
        { text: '排名', align: 'left', sortable: false, value: 'ranking' },
        { text: '帳號', align: 'left', sortable: false, value: 'account' },
        { text: '星星數量', sortable: false, value: 'tokenNum' }
      ],
      rankData: [],
      // mission dialog
      missionDialog: false,
      // loginIcon: 'fas fa-square',
      missionData: {
        'loginMission': false, // 登入任務 +50
        'completeGameTimes': 0, // 完成一個遊戲的次數(最多3次) +10
        'allCompleteMission': false, // 所有遊戲都完成 +20
        'levelUpTimesMission': 0 // 遊戲升級次數(最多6次) +20
      }
    }
  },
  mounted() {
    this.getUserInfo();
    this.getWeek();
    this.getDailyMission();
  },
  computed: {
    loginIcon() {
      if (this.missionData.loginMission == true) return 'fas fa-check-square';
      else return 'far fa-square'
    },
    allCompleteIcon() {
      if (this.missionData.allCompleteMission == true) return 'fas fa-check-square';
      else return 'far fa-square'
    }
  },
  methods: {
    logout() {
      axios.post('/api/logout').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.$router.push('/login');
        }
      });
    },
    getUserInfo() {
      axios.get('/api/getUserInfo').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.account = res.result.account;
          this.name = res.result.name;
          this.authority = res.result.authority;

          // rank
          this.getRank();
          if (this.authority == 'userTest') {
            this.authCHIN = '實驗組';
          } else {
            this.authCHIN = '對照組';
          }
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
    getRank() {
      axios.get('/api/rank/getRank', {
        params: {
          authority: this.authority
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
        }
      });
    },
    getDailyMission() {
      axios.get('/api/user/dailyMission').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.missionData = res.result;
        }
      })
    }
  }
}
</script>

<style>
#rank-table thead{
  background-color: orange;
  color: white;
}

#rank-table thead th{
  color: white;
  font-size: 14px;
}

#mission-card .v-input--selection-controls__input {
  color: white !important;
}

#mission-card .v-tooltip__content.menualble__content__active .theme--light.v-input--is-disabled .v-label, .theme--light.v-input--is-disabled input {
  /* color: #000 !important;  */
  /* color: white !important; */
  color: rgba(255,255,255,1) !important;
}

#mission-card .v-tooltip__content.menualble__content__active .theme--light.v-input--selection-controls.v-input--is-disabled .v-icon {
  /* color: #1976D2 !important; */
  /* color: white !important; */
  color: rgba(255,255,255,1) !important;
}
</style>
