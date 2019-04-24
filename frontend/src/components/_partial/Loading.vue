<template>
<div>
  <v-dialog v-model="dialog" hide-overlay persistent width="300">
    <v-card color="primary" dark>
      <v-card-text>
        {{text}}
        <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>
</div>
</template>

<script>
export default {
  components: {},
  props: ['parentToChild', 'parentText'],
  data() {
    return {
      text: ''
    }
  },
  mounted() {
    this.text = this.parentText;
  },
  computed: {
    dialog() {
      return this.parentToChild;
    }
  }
}
</script>