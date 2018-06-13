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
              <v-data-table
              :headers="damageHeaders"
              :items="orderDamageTable"
              hide-actions
              class="elevation-1"
              >
                <template slot="items" slot-scope="props">
                  <td>{{ props.item.timestamp }}</td>
                  <td class="text-xs-right">{{ props.item.orderNumber }}</td>
                  <td class="text-xs-right">{{ props.item.orderTotal }}</td>
                  <td class="text-xs-right">{{ props.item.reasonLost }}</td>
                </template>
              </v-data-table>
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
import moment from 'moment'

export default {
  name: 'ViewOrderDamages',
  data() {
    return {
      orderDamages: null,
      damageHeaders: [
        { text: 'Date', value: 'timestamp' },
        { text: 'Ebay Order', value: 'orderNumber' },
        { text: 'Order Total', value: 'orderTotal' },
        { text: 'Reason Lost', value: 'reasonLost' }
      ],
      orderDamageTable: [
        {
          damageDept: 'order',
          itemCost: 0.25,
          itemType: 'makeup',
          itemsLost: '123',
          orderNumber: '123',
          orderTotal: '123',
          reasonLost: 'Returned Product',
          shippingCost: '123',
          shippingLost: '123',
          timestamp: 1528846945595,
          value: false
        },
        {
          damageDept: 'order',
          itemCost: 0.25,
          itemType: 'makeup',
          itemsLost: '123',
          orderNumber: '123',
          orderTotal: '123',
          reasonLost: 'Returned Product',
          shippingCost: '123',
          shippingLost: '123',
          timestamp: 1528846945595,
          value: false
        }
      ],
      desserts: [
        {
          value: false,
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1%'
        }
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
        this.orderDamages = {}

        snapshot.forEach(doc => {
          this.orderDamages[doc.id] = doc.data()
          this.orderDamages[doc.id].value = false
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
