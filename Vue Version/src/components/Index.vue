// TODO consider adding an animation that shows the new tally being added to the total before updating
// TODO add transition/loading animations
// TODO add button for View Damages
// TODO make hover/mouseover on the loss sections do something to indicate it is a button/clickable
// TODO Add updated message when saving edited items
<template>

    <v-container  class="index" text-xs-center fill-height v-if="dataLoaded">
      <v-layout row wrap align-center justify-center>
        <v-flex xs12 sm10>
          <v-card class="elevation-12">
            <v-card class="elevation-5">
              <router-link :to="{ name: totalDamages.order.slug}">
              <h2>Total Order Losses</h2>
              <p class="loss loss-money">${{ totalDamages.order.total }}</p>
              <v-layout row wrap>
                <v-flex class="loss">
                  Item Losses:  <span class="loss-money">${{ totalDamages.order.itemTotal }}</span>
                </v-flex>
                <v-flex class="loss">
                  Shipping Losses:  <span class="loss-money">${{ totalDamages.order.shipTotal }}</span>
                </v-flex>
              </v-layout>
            </router-link>
            </v-card>
            <v-card class="elevation-3">
            <router-link :to="{ name: totalDamages.warehouse.slug}">
              <h2>Total Warehouse Losses</h2>
              <p class="loss loss-money">${{ totalDamages.warehouse.total }}</p>
            </router-link>
          </v-card>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'Index',
  data() {
    return {
      totalDamages: null,
      dataLoaded: false
    }
  },
  created() {
    // fetch data from firestore
    db
      .collection('totalLosses')
      .get()
      .then((this.totalDamages = {}))
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.totalDamages[doc.id] = doc.data()
        })
        this.dataLoaded = true
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style>
.index h2 {
  font-size: 2.2em;
}
.loss {
  font-size: 2em;
}
.loss-money {
  color: red;
}
.index a {
  color: black;
  text-decoration: none;
}
.index a:hover {
  color: #4676c4;
}
</style>
