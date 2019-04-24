<template>
<div>
  <v-snackbar
      v-model="msgFlag"
      :bottom="y === 'bottom'"
      :left="x === 'left'"
      :multi-line="mode === 'multi-line'"
      :right="x === 'right'"
      :timeout="timeout"
      :top="y === 'top'"
      :vertical="mode === 'vertical'"
      :color='color'
    >
      {{ text }}
      <v-btn
        color="white"
        flat
        @click="closeFlag=false"
      >
        Close
      </v-btn>
    </v-snackbar>
</div>
</template>

<script>
export default {
  components: {},
  props: ['parentFlag', 'parentColor', 'parentText'],
  data() {
    return {
      closeFlag: false,
      y: 'top',
      x: null,
      mode: '',
      timeout: 6000,
      text: '',
      color: ''
    }
  },
  mounted() {
    this.color = '#'+this.parentColor;
    this.text = this.parentText;
  },
  computed: {
    snackbar() {
      this.closeFlag = this.parentFlag;
      return this.parentFlag;
    },
    msgFlag() {
      return this.snackbar&&this.closeFlag;
    }
  }
}
</script>