<template>
  <v-layout row wrap align-center justify-center>
    <spinner></spinner>
  </v-layout>
</template>

<script>
import Spinner from 'vue-loading-spinner/src/components/Circle4.vue'

export default {
  name: 'Loading',
  components: {
    Spinner
  },
  data() {
    return {}
  }
}
</script>
