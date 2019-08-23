<template>
<div>
<v-app>
  <nav-header-user-game></nav-header-user-game>
  <v-content>

    <v-alert class="game-alert" v-model="alertFlag" dismissible type="info">
      {{ alertContent }}
    </v-alert>
    <v-container fluid >
      
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
      sourceLoader: '',
      // alert
      alertFlag: true, // 遊戲的提醒條
      alertContent: ''
    }
  },
  created() {
    this.gameNameEN = this.$route.params.gameNameEN;
    this.sourceJson = '/static/'+ this.gameNameEN + '/Build/'+ this.gameNameEN +'.json';
    this.sourceLoader = '/static/'+ this.gameNameEN +'/Build/UnityLoader.js';
  },
  mounted() {
    this.checkLogin();
    this.checkIsComplete();
    this.setAlert();
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
    },
    setAlert() {
      let gameName = this.gameNameEN.split("_")[0];
      
      if (gameName == 'PrePet') {
        this.alertContent = '按照彈跳的順序點選';
      } else if (gameName == 'BackPet') {
        this.alertContent = '按照彈跳的"相反順序"點選';
      } else if (gameName == 'PreAnimal') {
        this.alertContent = '按照動物聲音的順序點選';
      } else if (gameName == 'BackAnimal') {
        this.alertContent = '按照動物聲音的"相反順序"點選';
      } else if (gameName == 'Where') {
        this.alertContent = '綠色松果：松果尖端方向。褐色松果：松果移動方向'
      } else {
        this.alertFlag = false;
      }
    }
  }
}
</script>

<style>
.game-alert {
  position: absolute !important;
  right: 0px;
  z-index: 2000;
  font-size: 20px;
}
</style>

