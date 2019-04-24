<template>
<div>
<v-app>
  <nav-header-parent></nav-header-parent>
  <v-content>
    <v-container>
      <v-card>
        <v-card-title class="headline font-weight-medium blue-grey white--text">請協助評估孩子今天的訓練情形</v-card-title>
        <v-container>
          <v-subheader class="pa-0 title">1. 在注意力方面</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md1><span class="grey--text text--darken-3">很不專心</span></v-flex>
              <v-flex md10 class="pr-0">
                <v-slider v-model="focusValue" thumb-label="always" style="width:100%" :disabled="!canDo"></v-slider>
              </v-flex>
              <v-flex md1><span class="grey--text text--darken-3">很專心</span></v-flex>
              <v-flex shrink style="width: 60px">
                <v-text-field v-model="focusValue" class="mt-0" hide-details single-line type="number" :disabled="!canDo"></v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="pt-0">
          <v-subheader class="pa-0 title">2. 在情緒穩定度方面</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md1><span class="grey--text text--darken-3">很不穩定</span></v-flex>
              <v-flex md10 class="pr-0">
                <v-slider v-model="emotionValue" thumb-label="always" style="width:100%" :disabled="!canDo"></v-slider>
              </v-flex>
              <v-flex md1><span class="grey--text text--darken-3">很穩定</span></v-flex>
              <v-flex shrink style="width: 60px">
                <v-text-field v-model="emotionValue" class="mt-0" hide-details single-line type="number" :disabled="!canDo"></v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="pt-0">
          <v-subheader class="pa-0 title">3. 在訓練動機上</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md1><span class="grey--text text--darken-3">很沒有動機</span></v-flex>
              <v-flex md10 class="pr-0">
                <v-slider v-model="motivationValue" thumb-label="always" style="width:100%" :disabled="!canDo"></v-slider>
              </v-flex>
              <v-flex md1><span class="grey--text text--darken-3">很有動機</span></v-flex>
              <v-flex shrink style="width: 60px">
                <v-text-field v-model="motivationValue" class="mt-0" hide-details single-line type="number" :disabled="!canDo"></v-text-field>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="py-0">
          <v-subheader class="pa-0 title">4. 有無回饋的訊息</v-subheader>
          <v-card-text>
            <v-layout row>
              <v-flex md12>
                <v-textarea box name="input-7-4" label="感謝您提供寶貴的建議與回饋" v-model="feedback" :disabled="!canDo"></v-textarea>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-container>
        <v-container class="pt-0 mt-0">
          <v-layout row>
            <v-flex md12 v-if="canDo">
              <v-btn large :loading="loading" :disabled="loading" color="blue-grey" class="white--text" @click="submit" style="float: right;">
              完成<v-icon right dark>cloud_upload</v-icon>
            </v-btn>
            </v-flex>
          </v-layout>
        </v-container>   
      </v-card>
    </v-container>
  </v-content>

  <message :parentFlag="completeMessage" parentColor='8BC34A' parentText='您的回饋已經確實收到！'></message>
  <message :parentFlag="errorMessage" parentColor='EF5350' parentText='發送錯誤！'></message>
</v-app>
</div>
</template>

<script>
import NavHeaderParent from '@/components/NavHeaderParent'
import Message from '@/components/_partial/Message.vue'

export default {
  components: {
    NavHeaderParent,
    Message
  },
  data() {
    return {
      focusValue: 0, // 1.專注力
      emotionValue: 0, // 2.情緒穩定度
      motivationValue: 0, // 3.訓練動機
      feedback: '', //4.回饋
      loading: false,
      // message
      completeMessage: false,
      errorMessage: false,
      canDo: true
    }
  },
  mounted() {
    this.checkDailyPSQ();
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
            this.$router.push('/admin/index')
          } else if (res.result.authority=='parentTest' || res.result.authority=='parentComp') {
            // pass
          }
        } else {
          this.$router.push('/login');
        }
      });
    },
    checkDailyPSQ() {
      axios.get('/api/parent/checkDailyPSQ').then((response)=> {
        let res = response.data;
        if(res.status=='200') {
          if(res.result.canDo==true) {
            this.canDo = true;
          } else {
            this.canDo = false;
            this.focusValue = parseInt(res.result.focusValue);
            this.emotionValue = parseInt(res.result.emotionValue);
            this.motivationValue = parseInt(res.result.motivationValue);
            this.feedback = res.result.feedback;
          }
        }
      })
    },
    submit() {
      this.loading = true;

      axios.post('/api/parent/sendPSQ', {
        focusValue: this.focusValue.toString(),
        emotionValue: this.emotionValue.toString(),
        motivationValue: this.motivationValue.toString(),
        feedback: this.feedback
      }).then((response)=> {
        let res = response.data;
        if(res.status=='200') {
          this.completeMessage = true;
          this.loading = false;
          this.checkDailyPSQ();
        } else {
          this.loading = false;
          this.errorMessage = false;
          console.log(res.result);
        }
      });
    }
  }
}
</script>