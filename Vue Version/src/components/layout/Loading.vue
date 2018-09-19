<template>
  <v-layout row wrap align-center justify-center>
    <!-- <spinner></spinner> -->
    <v-progress-circular
      :size="70"
      :width="7"
      color="green"
      indeterminate
    ></v-progress-circular>
  </v-layout>
</template>

<script>
export default {
  name: 'Loading',
  data() {
    return {}
  }
}
</script>
