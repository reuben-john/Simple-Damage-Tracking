// TODO consider adding an animation that shows the new tally being added to the total before updating

<template>

    <v-container  class="index" text-xs-center fill-height v-if="totalDamages">
      <v-layout row wrap align-center>
        <v-flex xs12 mb-3>
          <v-card>
            <router-link :to="{ name: totalDamages.order.slug}">
              <h2>Total Order Losses</h2>
              <p class="loss loss-money">${{ totalDamages.order.total }}</p>
              <v-layout row wrap>
                <v-flex align-start text-xs-left offset-xs1 class="loss">
                  Item Losses:  <span class="loss-money">${{ totalDamages.order.itemTotal }}</span>
                </v-flex>
                <v-flex align-start text-xs-left class="loss">
                  Shipping Losses:  <span class="loss-money">${{ totalDamages.order.shipTotal }}</span>
                </v-flex>
              </v-layout>
            </router-link>
          </v-card>

        </v-flex>
        <v-flex xs12>
          <v-card>
            <router-link :to="{ name: totalDamages.warehouse.slug}">
              <h2>Total Warehouse Losses</h2>
              <p class="loss loss-money">${{ totalDamages.warehouse.total }}</p>
            </router-link>
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
.index h2 {
  font-size: 2em;
}
.index .card-content {
  text-align: center;
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
</style>
