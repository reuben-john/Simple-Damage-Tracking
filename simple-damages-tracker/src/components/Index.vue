<template>
  <div class="index container">
    <div class="card" v-for="(value, key, index) in totalDamages" :key="index">
      <div class="card-content">
        <h5>Total {{key | capitalize}} Damages</h5>
        <p class="loss">${{ value }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'Index',
  data() {
    return {
      totalDamages: null
    }
  },
  created() {
    // fetch data from firestore
    db
      .collection('appData')
      .doc('totalLosses')
      .get()
      .then(totals => {
        this.totalDamages = totals.data()
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.index {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 30px;
  margin-top: 60px;
}
.loss {
  font-size: 2em;
  color: red;
}
</style>
