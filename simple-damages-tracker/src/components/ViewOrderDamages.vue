<template>
<div class="view-order-damages">

  <v-container text-xs-center>
      <v-layout row wrap align-center>
        <v-flex xs12 sm6 offset-sm1 offset-md2>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>View Order Damagest</h1>
              </v-flex>
            </v-card-title>
            <v-card-text v-if="orderDamages">
              <v-flex
              v-for="report in orderDamages"
              :key="report.id"
              >

                <p>{{report}}</p>
              </v-flex>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
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

