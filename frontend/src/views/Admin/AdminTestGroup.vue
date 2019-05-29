<template>
<div>
<v-app>
  <nav-header-admin></nav-header-admin>
  <v-content>
    <v-container fluid>
      <!-- <v-btn :loading="loading3" :disabled="loading3" color="blue-grey" class="white--text" @click="loader = 'loading3'">下載資料
        <v-icon right dark>cloud_download</v-icon>
      </v-btn> -->
      <v-card>
        <v-card-title class="display-1">實驗組使用者
          <v-spacer></v-spacer>
          <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="userTestData" :search="search" :rows-per-page-items="[10, 20]">
          <template slot="items" slot-scope="props">
            <td>{{ props.item.name }}</td>
            <td class="text-xs">{{ props.item.calories }}</td>
            <td class="text-xs">{{ props.item.fat }}</td>
            <td class="text-xs">{{ props.item.carbs }}</td>
            <td class="text-xs">{{ props.item.protein }}</td>
            <td class="text-xs">{{ props.item.iron }}</td>
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
import NavHeaderAdmin from '@/components/NavHeaderAdmin'

export default {
  components: {
    NavHeaderAdmin
  },
  data() {
    return {
      search: '',
      headers: [
        {
          text: '姓名 (帳號)',
          align: 'left',
          sortable: false,
          value: 'name'
        },
        { text: '正序寵物樂園', value: 'PrePet' },
        { text: '逆序寵物樂園', value: 'BackPet' },
        { text: '正序動物農莊', value: 'PreAnimal' },
        { text: '逆序動物農莊', value: 'BackAnimal' },
        { text: '老師點點名', value: 'Teacher' },
        { text: '橡果去哪兒', value: 'Where' },
        { text: '球球滿天飛', value: 'Ball' }
      ],
      userTestData: [
        {
          name: '吉娃娃 (123)',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1%'
        },
        {
          name: 'Ice cream sandwich',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          iron: '1%'
        },
        {
          name: 'Eclair',
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          iron: '7%'
        },
        {
          name: 'Cupcake',
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          iron: '8%'
        },
        {
          name: 'Gingerbread',
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          iron: '16%'
        },
        {
          name: 'Jelly bean',
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          iron: '0%'
        },
        {
          name: 'Lollipop',
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          iron: '2%'
        },
        {
          name: 'Honeycomb',
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          iron: '45%'
        },
        {
          name: 'Donut',
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          iron: '22%'
        },
        {
          name: 'KitKat',
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          iron: '6%'
        }
      ]
    }
  },
  mounted() {
    this.checkLogin();
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
    }
  }
}
</script>