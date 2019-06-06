<template>
<div>
<v-app>
  <nav-header-user-game></nav-header-user-game>
  <v-content>
    <v-container fluid grid-list-md grid-list-sm>
      <unity :src="sourceJson" :unityLoader="sourceLoader" ref="myInstance"></unity>
    </v-container>
  </v-content>
</v-app>
</div>
</template>

<script>
import axios from 'axios'

import NavHeaderUserGame from '@/components/NavHeaderUserGame'
import NavFooterSimple from '@/components/NavFooterSimple'
import Unity from 'vue-unity-webgl'
import '@/assets/css/unity-game.css'

export default {
  components: {
    NavHeaderUserGame,
    NavFooterSimple,
    Unity
  },
  data() {
    return {
     gameNameEN: '',
     sourceJson: '',
     sourceLoader: ''
    }
  },
  created() {
    this.gameNameEN = this.$route.params.gameNameEN;
    this.sourceJson = '/static/'+ this.gameNameEN + '/Build/'+ this.gameNameEN +'.json';
    this.sourceLoader = '/static/'+ this.gameNameEN +'/Build/UnityLoader.js';
  },
  beforeCreate() {
    
  },
  mounted() {
    this.checkLogin();
    this.checkIsComplete();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.result.status == true) {
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
    checkIsComplete() {
      axios.get('/api/user/getGameIsComplete', {
        params: {
          gameNameEN: this.gameNameEN.split("_")[0]
        }
      }).then((response) => {
        let res = response.data;
        if (res.status == '200') {
          if(res.result.complete==true) {
            alert('今天不行玩了喔！');
            this.$router.push('/user/index');
          }
        }
      })
    }
  }
}
</script>

<style>
</style>
