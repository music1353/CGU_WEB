<template>
<div>
  <v-navigation-drawer :clipped="clipped" v-model="drawer" enable-resize-watcher app dark class="lighten-3">
    <v-list>
      <v-link-group v-for="item in items" :value="item.icon" :key="item.title">
        <v-list-tile :to="item.linkto" active-class="grey darken-4">
          <v-list-tile-action>
              <v-icon> {{item.icon}} </v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title> {{item.title}}</v-list-tile-title>
          </v-list-tile-content> 
        </v-list-tile>
      </v-link-group>
    </v-list>
  </v-navigation-drawer> 
  <v-toolbar fixed app :clipped-left="clipped" dark color="grey darken-3">
    <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
    <v-toolbar-title class="white--text"><a href="/admin/index" class="white--text" style="text-decoration: none;">管理員後台</a></v-toolbar-title>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
      <v-btn flat class="title">歡迎，{{name}}</v-btn>
      <v-btn color="orange darken-2" @click="logout">
        登出<v-icon dark right>logout</v-icon>
      </v-btn>
  </v-toolbar>
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
        'title': '今日練習狀況',
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
      }]
    }
  },
  mounted() {
    this.getUserInfo();
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
    }
  }
}
</script>