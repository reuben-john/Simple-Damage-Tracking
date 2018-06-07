<template>
  <div class="add-damages container">
    <h2 class="center-align">Add New Damages</h2>
    <form @submit.prevent="addDamages" v-for="(reason, index) in damageReasons" :key="index">
    </form>
  </div>
</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'AddDamages',
  data() {
    return {
      damageReasons: null,
      checked: true
    }
  },
  method: {
    addDamages() {}
  },
  created() {
    // fetch data from firestore
    db
      .collection('appData')
      .doc('damageReasons')
      .get()
      .then(reasons => {
        this.damageReasons = reasons.data()
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style>
</style>
