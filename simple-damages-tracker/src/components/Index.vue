<template>
  <div class="index container">
    <h2>Index</h2>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      totalDamages: {
        shipping: '',
        product: '',
        warehouse: ''
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.index {
  margin: 20px auto;
}
.collection {
  margin: 0 auto;
}
</style>
