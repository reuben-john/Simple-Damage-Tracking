<template>
<div class="view-order-damages">
  <h2>View Order Damages</h2>
</div>
</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'ViewOrderDamages',
  data() {
    return {
      orderDamages: null
    }
        },
  created() {
    let damagesRef = db.collection('damages').orderBy('timestamp')
    // fetch data from firestore
    let querty = damagesRef
      .where('damageDept', '==', 'order')
      .get()
      .then(snapshot => {
        // Make orderDamages an object to add the damage reports to it
        this.orderDamages = {}

        snapshot.forEach(doc => {
          this.orderDamages[doc.id] = doc.data()
          console.log(this.orderDamages[doc.id])
        })
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style>
</style>

