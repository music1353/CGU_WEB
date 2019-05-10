<template>
<div>
  <v-toolbar fixed app dark color="grey darken-3">
    <v-toolbar-title class="white--text"><a href="/parent/index" class="white--text" style="text-decoration: none;">長庚大學</a></v-toolbar-title>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
      <v-btn flat class="title">歡迎，{{ name }}</v-btn>
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
      authority: ''
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