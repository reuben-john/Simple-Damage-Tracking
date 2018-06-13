<template>
<div class="view-order-damages">

  <v-container text-xs-center>
      <v-layout row wrap align-center>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>View Order Damagest</h1>
              </v-flex>
            </v-card-title>
            <v-card-text v-if="orderDamages">
              <v-data-table
              :headers="orderHeaders"
              :items="orderDamages"
              hide-actions
              class="elevation-1"
              >
                <template slot="items" slot-scope="props">
                  <td class="text-xs-left">{{ props.item.timestamp }}</td>
                  <td class="text-xs-left">{{ props.item.orderNumber }}</td>
                  <td class="text-xs-left">${{ props.item.orderTotal }}</td>
                  <td class="text-xs-left">${{ props.item.shippingCost }}</td>
                  <td class="text-xs-left">${{ props.item.shippingLost }}</td>
                  <td class="text-xs-left">{{ props.item.itemType }}</td>
                  <td class="text-xs-left">{{ props.item.itemsLost }}</td>
                  <td class="text-xs-left">{{ props.item.reasonLost }}</td>
                </template>
              </v-data-table>
              <v-flex
              v-for="report in orderDamages"
              :key="report.id"
              >

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
import moment from 'moment'

export default {
  name: 'ViewOrderDamages',
  data() {
    return {
      orderDamages: null,
      orderHeaders: [
        { text: 'Date', value: 'timestamp' },
        { text: 'Ebay Order', value: 'orderNumber' },
        { text: 'Order Total', value: 'orderTotal' },
        { text: 'Shipping Cost', value: 'shippingCost' },
        { text: 'Shipping Lost', value: 'shippingLost' },
        { text: 'Item Type', value: 'itemType' },
        { text: 'Items Lost', value: 'itemsLost' },
        { text: 'Reason Lost', value: 'reasonLost' }
      ]
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
        this.orderDamages = []

        snapshot.forEach(doc => {
          let report = doc.data()
          report.id = doc.id
          report.value = false
          report.timestamp = moment(report.timestamp).format('LL')
          this.orderDamages.push(report)
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
