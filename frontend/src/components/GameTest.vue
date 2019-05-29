<template>
<div>
  <unity src="/static/WebTest/Build/WebTest.json" width="1000" height="600" unityLoader="/static/WebTest/Build/UnityLoader.js" ref="myInstance"></unity>

  <!-- <div class="webgl-content">
    <div id="gameContainer" style="width: 960px; height: 600px"></div>
    <div class="footer">
      <div class="webgl-logo"></div>
      <div class="fullscreen" @click="fullscreen"></div>
      <div class="title">PrePetWeb1</div>
    </div>
  </div> -->
</div>
</template>

<script>
import Unity from 'vue-unity-webgl'
// import '@/../static/WebTest/TemplateData/style.css'

export default {
  components: {
    Unity
  },
  data() {
    return {
      gameNameEN: 'PrePet'
    }
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
          if (res.result.authority == 'user') {
            // pass
            this.account = res.result.account;
          } else if (res.result.authority == 'admin') {
            this.$router.push('/admin/index');
          } else if (res.result.authority == 'parent') {
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
          gameNameEN: this.gameNameEN
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