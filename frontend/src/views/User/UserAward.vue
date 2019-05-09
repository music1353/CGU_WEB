<template>
<div>
<v-app>
  <nav-header-user></nav-header-user>
  <v-content>
    <v-container fluid grid-list-md grid-list-sm>
      <div>
        <i class="fas fa-star award-icon"></i>
        恭喜你！ 已經獲得 <span style="color: #FFC107; font-weight: bold;">{{tokenNum}}</span> 個星星了!
      </div>
      <!-- <div id="award-box">
        <div class="award-center">
          <i class="fas fa-star award-icon"></i>
          <p class="award-text">恭喜你！ 已經獲得 <span style="color: #FFC107; font-weight: bold;">{{tokenNum}}</span> 個星星了!</p>
        </div>
      </div> -->
    </v-container>
    <nav-footer-simple></nav-footer-simple>
  </v-content>
</v-app>
</div>
</template>

<script>
import axios from 'axios'

import NavHeaderUser from '@/components/NavHeaderUser'
import NavFooterSimple from '@/components/NavFooterSimple'

export default {
  components: {
    NavHeaderUser,
    NavFooterSimple
  },
  data() {
    return {
      tokenNum: ''
    }
  },
  mounted() {
    this.checkLogin();
    this.getTokenNum();
  },
  methods: {
    checkLogin() {
      axios.get('/api/checkLogin').then((response) => {
        let res = response.data;
        if (res.status == "200") {
          if (res.result.authority=='userTest' || res.result.authority=='compTest') {
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
    getTokenNum() {
      axios.get('/api/token/getTokenNum').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          this.tokenNum = res.result.token;
        }
      });
    }
  }
}
</script>

<style>
  #award-box {
    height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  #award-box .award-center {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 80%;
    text-align: center;
  }

  #award-box .award-center .award-icon{
    width: 100%;
    font-size: 100px;
    color: #FFC107;
  }

  #award-box .award-center .award-text {
    line-height: 130px;
    font-size: 35px;
  }
  
</style>
