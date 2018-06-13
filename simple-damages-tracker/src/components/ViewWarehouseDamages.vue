<template>
<div class="view-warehouse-damages">

  <v-container text-xs-center>
      <v-layout row wrap align-center>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>View warehouse Damages</h1>
              </v-flex>
            </v-card-title>
            <v-card-text v-if="warehouseDamages">
              <v-data-table
              :headers="warehouseHeaders"
              :items="warehouseDamages"
              hide-actions
              class="elevation-1"
              >
                <template slot="items" slot-scope="props">
                  <td class="text-xs-left">{{ props.item.timestamp }}</td>
                  <td class="text-xs-left">{{ props.item.itemType }}</td>
                  <td class="text-xs-left">{{ props.item.itemsLost }}</td>
                  <td class="text-xs-left">{{ props.item.reasonLost }}</td>
                </template>
              </v-data-table>
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
  name: 'ViewWarehouseDamages',
  data() {
    return {
      warehouseDamages: null,
      warehouseHeaders: [
        { text: 'Date', value: 'timestamp' },
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
      .where('damageDept', '==', 'warehouse')
      .get()
      .then(snapshot => {
        // Make warehouse an object to add the damage reports to it
        this.warehouseDamages = []

        snapshot.forEach(doc => {
          let report = doc.data()
          report.id = doc.id
          report.value = false
          report.timestamp = moment(report.timestamp).format('LL')
          this.warehouseDamages.push(report)
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
