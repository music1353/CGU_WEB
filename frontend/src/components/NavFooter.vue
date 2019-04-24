<template>
<div>
  <v-footer dark class="orange darken-3 white--text text-md-center" height="auto">
    <v-layout justify-center row wrap>
      <v-flex lighten-2 py-3 text-xs-center white--text xs12>
        &copy; {{ new Date().getFullYear() }} — <strong>長庚大學職能治療系</strong>
      </v-flex>
    </v-layout>
  </v-footer>
</div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      icons: [
      'fab fa-facebook',
      'fab fa-twitter',
      'fab fa-google-plus',
      'fab fa-linkedin',
      'fab fa-instagram'
    ]
    }
  }
}
</script>