<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <!-- test group panel start -->
      <div class="test-group panel">
        <div class="panel-title">實驗組</div>
        <div class="panel-cards">
          <v-layout align-center justify-start row fill-height wrap>
            <v-flex layout lg2 md3 v-for="item in testGroupData" :key="item.account" style="margin: 7px;">
              <v-hover>
                <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
                  <v-card-title primary-title>
                    <div>
                      <div class="headline">{{ item.name }}</div>
                      <span class="grey--text">{{ item.account }}</span>
                    </div>
                  </v-card-title>
                  <v-card-actions>
                    <v-layout align-center justify-end style="height: 30px;">
                        <v-icon class="mr-1 light-green--text" v-if="item.complete==true">done</v-icon>
                        <v-icon class="mr-1" v-else>clear</v-icon>
                        <span class="subheading light-green--text" v-if="item.complete==true">done</span>
                        <span class="subheading grey--text" v-else>incomplete</span>
                      </v-layout>
                  </v-card-actions>
                </v-card>
              </v-hover>
            </v-flex>
          </v-layout>
        </div>
      </div>
      <!-- test group panel end -->
      <!-- comparison group panel start -->
      <div class="comparison-group panel">
        <div class="panel-title">對照組</div>
        <div class="panel-cards">
          <v-layout align-center justify-start row fill-height wrap>
            <v-flex layout lg2 md3 v-for="item in compGroupData" :key="item.account" style="margin: 7px;">
              <v-hover>
                <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="344">
                  <v-card-title primary-title>
                    <div>
                      <div class="headline">{{ item.name }}</div>
                      <span class="grey--text">{{ item.account }}</span>
                    </div>
                  </v-card-title>
                  <v-card-actions>
                    <v-layout align-center justify-end style="height: 30px;">
                      <v-icon class="mr-1 light-green--text" v-if="item.complete==true">done</v-icon>
                      <v-icon class="mr-1" v-else>clear</v-icon>
                      <span class="subheading light-green--text" v-if="item.complete==true">done</span>
                      <span class="subheading grey--text" v-else>incomplete</span>
                    </v-layout>
                  </v-card-actions>
                </v-card>
              </v-hover>
            </v-flex>
          </v-layout>
        </div>
      </div>
      <!-- comparison group panel end -->
    </v-container>
  </v-content>
</v-app>
</div>
</template>

<script>
import axios from 'axios'
import NavHeaderAdmin from '@/components/NavHeaderAdmin'
var date = new Date();

export default {
  components: {
    NavHeaderAdmin
  },
  data() {
    return {
      'date': new Date().toISOString().substr(0, 10),
      'testGroupData': [],
      'compGroupData': []
    }
  },
  mounted() {
    this.checkLogin();
    this.getDailyUsersInfo();
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
    getDailyUsersInfo() {
      axios.get('/api/admin/getDailyUsersInfo').then((response)=> {
        let res = response.data;
        if (res.status == "200") {
          res.result.forEach((element)=> {
            if(element['authority']=='userTest') {
              this.testGroupData.push(element);
            } else if(element['authority']=='userComp') {
              this.compGroupData.push(element);
            }
          });
        }
      });
    }
  }
}
</script>

<style>
  #daily-done-panel .date-title-block .date-title {
    color: rgb(29, 29, 155);
    font-size: 30px;
    font-weight: bold;
  }

  .panel .panel-title {
    font-size: 35px;
    font-weight: bold;
  }
  .panel .panel-cards {
    margin-top: 10px;
    margin-bottom: 30px;
  }
</style>
