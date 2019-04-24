<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid style="padding-bottom: 0;">
      <v-select v-model="select" :items="items" label="Solo field" solo style="width: 30%;"></v-select>
    </v-container>
    <v-container fluid style="padding-top: 0;">
      <v-card>
        <v-card-title class="display-1">{{ titleName }}
          <v-spacer></v-spacer>
          <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="filterTable" :search="search" :rows-per-page-items="[10, 20]">
          <template slot="items" slot-scope="props">
            <td>{{ props.item.name }}</td>
            <td class="text-xs">{{ props.item.authority }}</td>
            <td class="text-xs">{{ props.item.account }}</td>
            <td class="text-xs">{{ props.item.phone }}</td>
          </template>
          <v-alert v-slot:no-results :value="true" color="error" icon="warning">
            Your search for "{{ search }}" found no results.
          </v-alert>
        </v-data-table>
      </v-card>
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
      select: '不分類別',
      items: ['不分類別', '實驗組 (userTest)', '對照組 (userComp)', '實驗組家長 (parentTest)', '對照組家長 (parentComp)'],
      // table
      search: '',
      headers: [
        {
          text: '姓名',
          align: 'left',
          sortable: false,
          value: 'name'
        },
        { text: '類別', value: 'authority' },
        { text: '帳號', value: 'account' },
        { text: '聯絡電話', value: 'phone' }
      ],
      usersData: []
    }
  },
  computed: {
    titleName() {
      if(this.select=='不分類別') return '所有使用者';
      else if(this.select=='實驗組 (userTest)') return '實驗組使用者';
      else if(this.select=='對照組 (userComp)') return '對照組使用者';
      else if(this.select=='實驗組家長 (parentTest)') return '實驗組家長';
      else if(this.select=='對照組家長 (parentComp)') return '對照組家長';
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
      } else if (this.select == '實驗組家長 (parentTest)') {
        let tempData = [];
        data.forEach((element) => {
          if(element.authority == 'parentTest') {
            tempData.push(element);
          }
        });
        return tempData;
      } else if (this.select == '對照組家長 (parentComp)') {
        let tempData = [];
        data.forEach((element) => {
          if(element.authority == 'parentComp') {
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
    getUsers() {
      axios.get('/api/admin/getUsers').then((response)=> {
        let res = response.data;
        if (res.status == "200") {
          this.usersData = res.result;
        }
      });
    }
  }
}
</script>