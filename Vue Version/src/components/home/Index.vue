<template>
    <v-container class="index" text-xs-center fill-height>
      <loading v-if="loading"></loading>
      <v-layout row wrap align-center justify-center v-if="dataLoaded">
        <v-flex xs12 sm10>
          <v-card class="elevation-12">
            <v-card class="elevation-5">
              <router-link :to="{ name: totalDamages.order.slug}">
              <h2 class="pt-2">Total Order Losses</h2>
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
              <h2 class="pt-2">Total Warehouse Losses</h2>
              <p class="loss loss-money pb-2">${{ totalDamages.warehouse.total }}</p>
            </router-link>
          </v-card>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import db from '@/firebase/init'
import Loading from '@/components/layout/Loading'

export default {
  name: 'Index',
  components: {
    Loading
  },
  data() {
    return {
      totalDamages: null,
      dataLoaded: false,
      loading: true
    }
  },
  created() {
    // Display loading graphic during page load, closes it after last database call
    this.loading = true
    // fetch damage tallies from firestore
    db
      .collection('totalLosses')
      .get()
      .then((this.totalDamages = {}))
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.totalDamages[doc.id] = doc.data()
        })

        // Displays loading graphic for 800ms before showing table
        let vm = this
        setTimeout(() => {
          this.loading = false
          this.dataLoaded = true
        }, 800)
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
