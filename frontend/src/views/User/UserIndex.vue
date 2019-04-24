<template>
<div>
<v-app>
  <nav-header-user></nav-header-user>
  <v-content >
    <v-container fluid grid-list-md grid-list-sm>
      <v-layout v-if="doFlag" align-center justify-start row wrap class="mt-3">
        <v-flex layout xs12 md4 v-for="card in gamesCards" :key="card.title" class="px-3 mb-3">
          <v-hover>
            <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
              <v-img :aspect-ratio="16/9" :src="card.imgURL"></v-img>
              <v-card-title>
                <div>
                  <span class="headline"> {{card.gameNameCH}} </span>
                  <div class="d-flex">
                    <!-- <v-rating :value="card.value" color="amber" dense half-increments readonly size="14"></v-rating> -->
                    <div class="ml-2 grey--text text--darken-2">
                      <!-- <span>{{ card.value }}</span> -->
                      <span>({{ card.reviews }})</span>
                    </div>
                  </div>
                </div>
                <v-spacer></v-spacer>
                <v-btn icon class="mr-0" :to="card.link">
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-card-title>
            </v-card>
          </v-hover>
        </v-flex>
      </v-layout>
      <v-layout v-else>
        <v-jumbotron :gradient="gradient" dark src="https://cdn.vuetifyjs.com/images/parallax/material2.jpg" style="width: 100vw; height: 80vh;">
          <v-container fill-height>
            <v-layout align-center>
              <v-flex text-xs-center>
                <h3 class="display-3">今天沒有遊戲</h3>
                <div class="title mt-5">每週二、五記得來玩呦！</div>
              </v-flex>
            </v-layout>
          </v-container>
        </v-jumbotron>
      </v-layout>
    </v-container>
    <nav-footer-simple></nav-footer-simple>
  </v-content>
</v-app>
</div>
</template>

<script>
import NavHeaderUser from '@/components/NavHeaderUser'
import NavFooterSimple from '@/components/NavFooterSimple'

export default {
  components: {
    NavHeaderUser,
    NavFooterSimple
  },
  data() {
    return {
      doFlag: true,
      gamesCards: [],
      gradient: 'to top right, rgba(63,81,181, .7), rgba(25,32,72, .7)'
    }
  },
  mounted() {
    this.checkLogin();
    this.getGames();
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
    getGames() {
      axios.get('/api/user/getGames').then((response) => {
        let res = response.data;
        this.doFlag = res.msg;
        if (res.status == '200') {
          this.gamesCards = res.result;
        }
      });
    }
  }
}
</script>