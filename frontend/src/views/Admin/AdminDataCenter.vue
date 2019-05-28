<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <v-card>
        <v-container fluid>
          <div class="user-data mb-3">
            <p class="headline">使用者資料</p>
            <!-- <v-icon large color="green darken-2" class="mr-3" style="font-size: 25px;">fas fa-file-csv</v-icon> -->
            <v-btn color="#01579B" class="white--text ml-0" large @click="getUserData">
              使用者資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
            <v-btn color="#01579B" class="white--text ml-0" large @click="getParentData">
              家長資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
            <v-btn color="#01579B" class="white--text ml-0" large @click="getAdminData">
              管理員資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
          <v-divider></v-divider>
          <div class="game-data mt-3 mb-3">
            <p class="headline">遊戲資料</p>
            <v-btn color="#558B2F" class="white--text ml-0" large @click="getGameData">
              遊戲紀錄資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
          <v-divider></v-divider>
          <div class="game-data mt-3 mb-3">
            <p class="headline">問卷資料</p>
            <v-btn color="blue-grey" class="white--text ml-0" large @click="getQuestionnairesData">
              問卷資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
          <v-divider></v-divider>
          <div class="game-data mt-3 mb-3">
            <p class="headline">禮物兌換資料</p>
            <v-btn color="red darken-2" class="white--text ml-0" large @click="getGiftExchangeData">
              禮物兌換資料
              <v-icon right dark>cloud_download</v-icon>
            </v-btn>
          </div>
        </v-container>
      </v-card>
    </v-container>
  </v-content>
</v-app>
</div>
</template>
<script>
import axios from 'axios'
import { CsvExport } from '@/utils/CsvExport.js'
import * as jsonexport from "jsonexport/dist"
import fs from 'fs'
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
        if (res.status == "200") {
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
    json2csv(res, filename) {
      jsonexport(res, function(err, csv){
        if(err) return console.log(err);
        // console.log(csv);

        let Today = new Date();
        let fileName = Today.getFullYear()+'-'+(Today.getMonth()+1)+'-'+Today.getDate()+'-'+filename;

        let csvContent = "data:text/csv;charset=utf-8,\uFEFF" + csv;
        let encodedUri = encodeURI(csvContent);
        let link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `${(fileName || 'file')}.csv`);
        document.body.appendChild(link); // Required for FF
        link.click(); // This will download the data file named "my_data.csv".
        document.body.removeChild(link); // Required for FF
      });
    },
    getUserData() {
      axios.get('/api/data/user').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;
          this.json2csv(result, '使用者資料');
        }
      });
    },
    getParentData() {
      axios.get('/api/data/parent').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;
          this.json2csv(result, '家長資料');
        }
      });
    },
    getAdminData() {
      axios.get('/api/data/admin').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;
          this.json2csv(result, '管理員資料');
        }
      });
    },
    getGameData() {
      axios.get('/api/data/game').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;
          this.json2csv(result, '遊戲紀錄資料');
        }
      });
    },
    getQuestionnairesData() {
      axios.get('/api/data/questionnaires').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;
          this.json2csv(result, '問卷資料');
        }
      });
    },
    getGiftExchangeData() {
      axios.get('/api/data/giftExchange').then((response) => {
        let res = response.data;
        if (res.status == '200') {
          let result = res.result;
          this.json2csv(result, '禮物兌換資料');
        }
      });
    }
  }
}
</script>