<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid style="padding-top: 0;">
      
    </v-container>
  </v-content>
</v-app>
</div>
</template>
<script>
import axios from 'axios'
import NavHeaderAdmin from '@/components/NavHeaderAdmin'

export default {
  components: {
    NavHeaderAdmin
  },
  data() {
    return {
      
    }
  },
  mounted() {
    this.checkLogin();
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
  }
}
</script>