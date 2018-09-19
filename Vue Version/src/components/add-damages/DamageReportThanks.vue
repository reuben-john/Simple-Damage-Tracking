<template>
  <v-layout row wrap justify-center  class="damage-report-thanks">
    <v-flex xs12 sm8 >
      <h1>Your damage report has been logged!</h1>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'Damage Report Thanks',
  data() {
    return {}
  }
}
</script>

<style>
.damage-report-thanks h1 {
  color: green;
}
</style>
