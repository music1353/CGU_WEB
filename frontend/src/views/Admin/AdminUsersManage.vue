<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid style="padding-bottom: 0;">
      <v-layout>
        <v-flex md3>
          <v-select v-model="select" :items="items" label="Solo field" solo></v-select>
        </v-flex>
        <v-flex md2 class="ml-3 pb-2">
          <v-btn round color="#F57C00" class="white--text mt-2" @click="newOneDialog=true">新增使用者
            <v-icon right dark style="font-size: 15px;">fas fa-user-plus</v-icon>
          </v-btn>
        </v-flex>
        <!-- TODO: 批量新增 -->
        <v-flex md2 class="pb-2">
          <v-tooltip bottom>
              <v-btn slot="activator" round color="green darken-2" class="white--text mt-2" @click="handlFileUpload">批量新增
                <v-icon right dark style="font-size: 15px;">fas fa-file-csv</v-icon>
              </v-btn>
            <span>csv格式：身份 (test/comp), 姓名, 帳號, 密碼, 家長姓名, 家長帳號, 家長密碼, 聯絡電話</span>
          </v-tooltip>
          <input type="file" id="csvUpload" ref="csvUpload" accept=".csv" @change="getUploadFile">
        </v-flex>
         <message :parentFlag="csvFlag" :parentColor='csvColor' :parentText='csvMsg
  '></message>
        <!-- 批量新增 -->
      </v-layout>
    </v-container>

    <v-container fluid style="padding-top: 0;">
      <v-card>
        <v-card-title class="display-1">{{ titleName }}
          <v-spacer></v-spacer>
          <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="filterTable" :search="search" :rows-per-page-items="[10, 20]">
          <template slot="items" slot-scope="props">
            <td class="text-xs">{{ props.item.name }}</td>
            <td class="text-xs">{{ props.item.account }}</td>
            <td class="text-xs">{{ props.item.parentName }}</td>
            <td class="text-xs">{{ props.item.parentAccount }}</td>
            <td class="text-xs">
               <v-chip v-if="props.item.authority.indexOf('Test')>=0" color="primary" text-color="white" small>實驗組</v-chip>
               <v-chip v-else color="green" text-color="white" small>對照組</v-chip>
            </td>
            <td class="text-xs">{{ props.item.phone }}</td>
            <td class="text-xs">
              <v-icon small @click="setTempDelData(props.item)">delete</v-icon>
            </td>
          </template>
          <v-alert v-slot:no-results :value="true" color="error" icon="warning">
            Your search for "{{ search }}" found no results.
          </v-alert>
        </v-data-table>
      </v-card>
    </v-container>
  </v-content>

  <!-- 是否刪除用戶 dialog -->
  <v-dialog v-model="delOneUserDialog" persistent max-width="290">
    <v-card>
      <v-card-title class="headline">是否要刪除用戶 ?</v-card-title>
      <v-card-text>這個刪除行為將user及parent的帳戶一併刪除</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red darken-1" flat @click="delOneUserDialog=false">取消</v-btn>
        <v-btn color="red darken-1" flat @click="delOneUser">確定</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <message :parentFlag="delSuccessMsgFlag" parentColor='8BC34A' parentText='刪除帳戶成功！
  '></message>
  <message :parentFlag="delFailMsgFlag" parentColor='EF5350' parentText='刪除帳戶失敗！
  '></message>
  <!-- 是否刪除用戶 dialog -->

  <!-- 新增用戶 fullscreen dialog -->
  <v-dialog v-model="newOneDialog" fullscreen hide-overlay transition="dialog-bottom-transition">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="closeNewOneDialog">
          <v-icon>close</v-icon>
        </v-btn>
        <v-toolbar-title>新增使用者</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
          <v-btn dark flat @click="newOneUser">確定新增</v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card-text>
        <v-container grid-list-md>
          <v-layout wrap>
            <v-flex md6>
              <v-subheader class="pl-0 pr-1 title">此組帳號的身份</v-subheader>
              <v-select :items="authItems" solo box v-model="authSelect" style="width: 50%;" @change="changeAuth"></v-select>
            </v-flex>
          </v-layout>
          <v-divider></v-divider>
          <v-layout wrap>
            <!-- User資料區:左半邊  -->
            <!-- TODO: -->
            <v-flex md6>
              <v-subheader class="pl-0 mt-3 title">使用者資料</v-subheader>
              <v-form ref="userForm" v-model="userValid" lazy-validation>
                <v-text-field label="小朋友身份" v-model="addNewUserAuthority" required style="width: 80%;" disabled></v-text-field>
                <v-text-field label="小朋友姓名" v-model="addNewUserName" required :rules="nameRules" style="width: 80%;"></v-text-field>
                <v-text-field label="小朋友帳號" v-model="addNewUserAccount" required :rules="accountRules" :hint="addNewUserAccountHint" style="width: 80%;"></v-text-field>
                <v-text-field label="小朋友密碼" v-model="addNewUserPwd" required :rules="passwordRules" style="width: 80%;"></v-text-field>
              </v-form>
            </v-flex>
            <!-- User資料區:左半邊  -->
            <!-- Parent資料區:右半邊  -->
            <v-flex md6>
              <v-subheader class="pl-0 mt-3 title">家長資料</v-subheader>
              <v-form ref="parentForm" v-model="parentValid" lazy-validation>
                <v-text-field label="家長身份" v-model="addNewParentAuthority" required style="width: 80%;" disabled></v-text-field>
                <v-text-field label="家長姓名" v-model="addNewParentName" required :rules="nameRules" style="width: 80%;"></v-text-field>
                <v-text-field label="家長帳號" v-model="addNewParentAccount" :rules="accountRules" :hint="addNewParentAccountHint" required style="width: 80%;"></v-text-field>
                <v-text-field label="家長密碼" v-model="addNewParentPwd" required :rules="passwordRules"style="width: 80%;"></v-text-field>
                <v-text-field label="家長電話" v-model="addNewParentPhone" required :rules="phoneRules" style="width: 80%;"></v-text-field>
              </v-form>
            </v-flex>
            <!-- Parent資料區:右半邊  -->
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>
  <message :parentFlag="addSuccessMsgFlag" parentColor='8BC34A' parentText='新增帳戶成功！
  '></message>
  <message :parentFlag="addFailMsgFlag" parentColor='EF5350' :parentText='addFailErrMsg'></message>
  <!-- 新增用戶 fullscreen dialog -->

</v-app>
</div>
</template>
<script>
import axios from 'axios'
import Papa from 'papaparse'
import NavHeaderAdmin from '@/components/NavHeaderAdmin'
import Message from "@/components/_partial/Message.vue"

export default {
  components: {
    NavHeaderAdmin,
    Message
  },
  data() {
    return {
      // select
      select: '不分類別',
      items: ['不分類別', '實驗組 (userTest)', '對照組 (userComp)'],
      // table
      search: '',
      headers: [
        { text: '姓名', align: 'left', sortable: false, value: 'name' },
        { text: '帳號', value: 'account' },
        { text: '家長姓名', align: 'left', sortable: false, value: 'parentName' },
        { text: '家長帳號', value: 'parentAccount' },
        { text: '類別', value: 'authority' },
        { text: '聯絡電話', value: 'phone' },
        { text: '操作', sortable: false, value: 'name' }
      ],
      usersData: [],
      // 是否刪除用戶 dialog
      delOneUserDialog: false,
      tempDelUserAccount: '',
      tempDelParentAccount: '',
      delSuccessMsgFlag: false,
      delFailMsgFlag: false,
      //  TODO: 新增用戶 fullscreen dialog
      addSuccessMsgFlag: false,
      addFailMsgFlag: false,
      addFailErrMsg: '',
      newOneDialog: false,
      userValid: true,
      parentValid: true,
      authSelect: '實驗組',
      authItems: ['實驗組', '對照組'],
      addNewUserAuthority: 'userTest',
      addNewUserName: '',
      addNewUserAccount: '',
      addNewUserAccountHint: '建議使用 testXXXX 作為帳號',
      addNewUserPwd: '',
      addNewParentAuthority: 'parentTest',
      addNewParentName: '',
      addNewParentAccount: '',
      addNewParentAccountHint: '建議使用 parentTXXXX 作為帳號',
      addNewParentPwd: '',
      addNewParentPhone: '',
      nameRules: [
        v => !!v || '您還沒有填寫姓名'
      ],
      accountRules: [
        v => !!v || '您還沒有填寫帳號'
      ],
      passwordRules: [
        v => !!v || '您還沒有填寫密碼'
      ],
      phoneRules: [
        v => !!v || '您還沒有填寫密碼'
      ],
      // 批量新增使用者
      csvFlag: false,
      csvColor: '',
      csvMsg: '',
      csvFile: '',
    }
  },
  computed: {
    titleName() {
      if(this.select=='不分類別') return '所有使用者';
      else if(this.select=='實驗組 (userTest)') return '實驗組使用者';
      else if(this.select=='對照組 (userComp)') return '對照組使用者';
    },
    filterTable() {
      let data = this.usersData;
      if (this.select == '實驗組 (userTest)') {
        let tempData = [];
        data.forEach((element) => {
          if(element.authority == 'userTest') {
            tempData.push(element);
          }
        });
        return tempData;
      } else if (this.select == '對照組 (userComp)') {
        let tempData = [];
        data.forEach((element) => {
          if(element.authority == 'userComp') {
            tempData.push(element);
          }
        });
        return tempData;
      } else {
        return data;
      }
    }
  },
  mounted() {
    this.checkLogin();
    this.getUsers();
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
    getUsers() {
      axios.get('/api/admin/getUsers').then((response)=> {
        let res = response.data;
        if (res.status == "200") {
          this.usersData = res.result;
        }
      });
    },
    // 設置暫時的刪除資訊
    setTempDelData(item) {
      this.delOneUserDialog = true;
      this.tempDelUserAccount = item.account;
      this.tempDelParentAccount = item.parentAccount;
    },
    delOneUser() {
      this.delSuccessMsgFlag = false;
      this.delFailMsgFlag = false;

      axios.post('/api/admin/delOneUser', {
        account: this.tempDelUserAccount,
        Paccount: this.tempDelParentAccount
      }).then((response)=> {
        let res = response.data;
        if (res.status == "200") {
          this.delSuccessMsgFlag = true;
          this.delOneUserDialog = false;
          this.getUsers();
        } else {
          this.delFailMsgFlag = true;
        }
      });
    },
    // TODO: 新增使用者 Dialog (newOneDialog)
    changeAuth(item) {
      if (item == '實驗組') {
        this.addNewUserAuthority='userTest';
        this.addNewParentAuthority='parentTest';
        this.addNewUserAccountHint='建議使用 testXXXX 作為帳號'
        this.addNewParentAccountHint='建議使用 parentTXXXX 作為帳號'
      } else if (item == '對照組') {
        this.addNewUserAuthority='userComp';
        this.addNewParentAuthority='parentComp';
        this.addNewUserAccountHint='建議使用 compXXXX 作為帳號'
        this.addNewParentAccountHint='建議使用 parentCXXXX 作為帳號'
      }
    },
    closeNewOneDialog() {
      this.newOneDialog = false;
      this.$refs.userForm.resetValidation();
      this.$refs.parentForm.resetValidation();
      this.authSelect = '實驗組'
      this.addNewUserAuthority = 'userTest';
      this.addNewUserName = '';
      this.addNewUserAccount = '';
      this.addNewUserPwd = '';
      this.addNewParentAuthority = 'parentTest';
      this.addNewParentName = '';
      this.addNewParentAccount = '';
      this.addNewParentPwd = '';
      this.addNewParentPhone = '';
    },
    newOneUser() {
      if (this.$refs.userForm.validate() && this.$refs.parentForm.validate()) {
        this.addSuccessMsgFlag = false;
        this.addFailMsgFlag = false;

        axios.post('/api/admin/addOneUser', {
          authority: this.addNewUserAuthority, 
          account: this.addNewUserAccount,
          pwd: this.addNewUserPwd,
          name: this.addNewUserName,
          Pauthority: this.addNewParentAuthority,
          Paccount: this.addNewParentAccount,
          Ppwd: this.addNewParentPwd,
          Pname: this.addNewParentName,
          phone: this.addNewParentPhone
        }).then((response) => {
          let res = response.data;
          if (res.status == "200") {
            this.addSuccessMsgFlag = true;
            this.closeNewOneDialog();
            this.getUsers();
          } else {
            this.addFailErrMsg = res.msg;
            this.addFailMsgFlag = true;
          }
        });
      }
    },
    // TODO: 測試中
    handlFileUpload() {
      let uploadbtn = this.$refs.csvUpload;
      csvUpload.click();
    },
    getUploadFile() {
      let uploadbtn = this.$refs.csvUpload;
      this.csvFile = this.$refs.csvUpload.files[0];
      this.csvFlag = false;

      let self = this;
      let data = Papa.parse(this.csvFile, {
        header: true,
        complete(results) {
          // 檢測csv是否符合格式
          let keys = Object.keys(results.data[0]);
          if (keys.sort().toString() == ["身份", "姓名", "帳號", "密碼", "家長姓名", "家長帳號", "家長密碼", "聯絡電話"].sort().toString()) {
            console.log('符合格式');
            axios.post('/api/admin/addCsvUser', {
              csvData: results.data
            }).then((response) => {
              let res = response.data;
              if (res.status=='200') {
                self.csvColor = '8BC34A';
                self.csvMsg = res.msg;
                self.csvFlag = true;
                self.getUsers();
              } else {
                self.csvColor = 'EF5350';
                self.csvMsg = res.msg;
                self.csvFlag = true;
              }
            });
          } else {
            self.csvColor = 'EF5350';
            self.csvMsg = 'csv不符合格式！';
            self.csvFlag = true;
            console.log('csv不符合格式');
            uploadbtn.type = "text";
            uploadbtn.type = "file";
            self.csvFile = '';
          }
        },
        error(err, file, inputElem, reason) {
          console.log('上傳失敗: ' + reason);
        }
      });
    }
  }
}
</script>

<style scoped>
 #csvUpload {
   display: none;
 }
</style>
