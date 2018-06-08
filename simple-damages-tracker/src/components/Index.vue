<template>
  <div class="index container">
    <div class="card" v-if="totalDamages" v-for="(type, index) in totalDamages" :key="index">
      <div class="card-content">
        <router-link :to="{ name: type.slug}">
          <h5>{{type.name}} Losses</h5>
          <p class="loss">${{ type.total }}</p>
        </router-link>
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

<style>
.index {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 60px;
  margin-top: 60px;
}
.index .card-content {
  text-align: center;
}
.loss {
  font-size: 2em;
  color: red;
}
</style>
