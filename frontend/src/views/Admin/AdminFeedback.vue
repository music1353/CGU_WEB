<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <v-date-picker color="primary" v-model="date" full-width landscape reactive class="mt-0" @input="chooseDate"></v-date-picker>
      <v-select v-model="select" :items="items" label="Solo field" solo class="mt-4" style="width: 30%;"></v-select>
      <div class="feedback-cards">
        <v-layout align-center justify-start row fill-height>
          <v-flex layout xs12 md4 style="margin: 7px;" v-for="fb in filterTable" :key="fb.pAccount">
            <v-hover>
              <v-card slot-scope="{ hover }" :class="`elevation-${hover ? 12 : 2}`" class="mx-auto" width="500">
                <v-card-title class="mb-0 pb-0">
                  <span class="headline">{{ fb.pName }}</span>
                  <span class="grey--text ml-1">{{ fb.pAccount }}</span>
                </v-card-title>
                <v-layout>
                  <v-flex md6>
                    <v-card-text class="pb-0">
                      <v-tooltip top>
                        <v-icon slot="activator" dark color="primary">far fa-lightbulb</v-icon>
                        <span>專注度</span>
                      </v-tooltip>
                      <div class="subheading" style="display:inline-block; float: right;">{{ fb.focusValue }}</div>
                      <v-progress-linear color="success" height="5" :value="fb.focusValue"></v-progress-linear>
                    </v-card-text>
                  </v-flex>
                  <v-flex md6>
                    <v-card-text class="pb-0">
                      <v-tooltip top>
                        <v-icon slot="activator" dark color="primary">far fa-smile</v-icon>
                        <span>情緒穩定度</span>
                      </v-tooltip>
                      <div class="subheading" style="display:inline-block; float: right;">{{ fb.emotionValue }}</div>
                      <v-progress-linear color="success" height="5" :value="fb.emotionValue"></v-progress-linear>
                    </v-card-text>
                  </v-flex>
                  <v-flex md6>
                    <v-card-text class="pb-0">
                      <v-tooltip top>
                        <v-icon slot="activator" dark color="primary">far fa-paper-plane</v-icon>
                        <span>訓練動機</span>
                      </v-tooltip>
                      <div class="subheading" style="display:inline-block; float: right;">{{ fb.motivationValue }}</div>
                      <v-progress-linear color="success" height="5" :value="fb.motivationValue"></v-progress-linear>
                    </v-card-text>
                  </v-flex>
                </v-layout>
                <v-layout>
                </v-layout>
                <v-layout>
                  <v-flex md12>
                    <v-card-text class="pt-2 pb-0">
                      <v-icon slot="activator" dark color="primary">far fa-file-alt</v-icon>
                      <div class="subheading ml-1" style="display:inline-block;">意見回饋</div>
                      <p class="mt-1" style="height: 60px; overflow:auto;">{{ fb.feedback }}</p>
                    </v-card-text>
                  </v-flex>
                </v-layout>
              </v-card>
            </v-hover>
            
          </v-flex>
        </v-layout>
      </div>
      
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
      // select
      select: '實驗組',
      items: ['實驗組', '對照組'],
      date: '',
      feedbackData: []
    }
  },
  mounted() {
    this.checkLogin();
    this.initDate();
    this.initFeedback();
  },
  computed: {
    filterTable() {
      let data = this.feedbackData;
      if (this.select == '實驗組') {
        let tempData = [];
        data.forEach((element) => {
          if(element.pAuthority == 'parentTest') {
            tempData.push(element);
          }
        });
        return tempData;
      } else if (this.select == '對照組') {
        let tempData = [];
        data.forEach((element) => {
          if(element.pAuthority == 'parentComp') {
            tempData.push(element);
          }
        });
        return tempData;
      }
    }
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
    initDate() {
      let d = new Date();
      let month = d.getMonth()+1; 
      let day = d.getDate(); 
      this.date = d.getFullYear()+'-'+((month<10 ? '0' : ''))+month+'-'+((day<10 ? '0' : '') + day);
    },
    initFeedback() {
      axios.get('/api/admin/getFeedback', {
        params: {
          date: this.date.toString()
        }
      }).then((response) => {
        let res = response.data;
        if (res.status=='200') {
          this.feedbackData = res.result;
        }
      });
    },
    chooseDate(date) {
      axios.get('/api/admin/getFeedback', {
        params: {
          date: date
        }
      }).then((response) => {
        let res = response.data;
        if (res.status=='200') {
          this.feedbackData = res.result;
        }
      });
    }
  }
}
</script>

