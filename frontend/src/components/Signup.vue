<template>
<div>
  <section id="signup-block">
    <v-container>
      <v-layout align-center justify-center mt-5 mb-5>
        <v-flex md8 class="box-shadow">

          <!-- signup form start -->
          <v-layout justify-center>
            <v-flex md10>
              <h1 style="padding-top: 30px; font-size: 30px;">註冊</h1>
              <v-form ref="form" class="signup-form" v-model="valid" lazy-validation>
                <v-text-field v-model="account" :rules="accountRules" label="帳號" required></v-text-field>
                <v-text-field v-model="password" :rules="passswordRules" label="密碼" required type="password"></v-text-field>
                <v-text-field v-model="password" :rules="passswordRules" label="確認密碼" required type="password"></v-text-field>
                <v-text-field v-model="account" :rules="accountRules" label="帳號" required></v-text-field>
                <v-text-field v-model="password" :rules="passswordRules" label="密碼" required type="password"></v-text-field>
                <v-text-field v-model="password" :rules="passswordRules" label="確認密碼" required type="password"></v-text-field>
                <v-text-field v-model="account" :rules="accountRules" label="帳號" required></v-text-field>
                <v-text-field v-model="password" :rules="passswordRules" label="密碼" required type="password"></v-text-field>
                <v-text-field v-model="password" :rules="passswordRules" label="確認密碼" required type="password"></v-text-field>

              </v-form>
              <v-btn class="white--text" color="orange darken-1" :disabled="!valid" @click="submit" style="margin-bottom: 30px;">註冊</v-btn>
            </v-flex>
          </v-layout>
          <!-- signup form end -->
           
        </v-flex>
      </v-layout>
    </v-container>
  </section>
</div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      dialog: false,
    }
  }
}
</script>

<style>
#signup-block {
  /* background-image: url('./../assets/image/bg5.jpg');
  background-size: cover; */
  background-color: rgb(128, 129, 129);
}

#signup-block .signup-form {
  margin-top: 30px;
  margin-bottom: 20px;
}
</style>
