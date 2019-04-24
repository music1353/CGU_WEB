<template>
<div>
  <v-footer :absolute="footerABS">
    <v-layout justify-center row wrap>
      <div>&copy; {{ new Date().getFullYear() }} - <strong>長庚大學職能治療系</strong></div>
    </v-layout>
  </v-footer>
</div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      footerABS: true
    }
  }
}
</script>