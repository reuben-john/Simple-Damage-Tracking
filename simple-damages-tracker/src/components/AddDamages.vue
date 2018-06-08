<template>
  <div class="add-damages">
    <v-container>
      <v-layout row wrap>
        <v-flex xs12 sm6 offset-sm3>
          <v-card width="600">
            <v-card-title primary-title>
              <v-flex text-xs-center>
                <h1>Add Damage Report</h1>
              </v-flex>
            </v-card-title>
            <v-card-text v-if="damageReasons">
              <v-radio-group v-model="damageReport.damageDept">
                <v-radio
                  v-for="(value, key) in damageReasons"
                  :key="key"
                  :label="`Add new ${key} damage report`"
                  :value="key"
                ></v-radio>
                <h2>{{damageDept}}</h2>
              </v-radio-group>
              <v-layout v-if="damageReport.damageDept == 'order'">
                <v-flex xs8 sm4 offset-sm1>
                  <v-select
                    :items="damageReasons.order.type"
                    v-model="damageReport.reasonLost"
                    label="Damage Type"
                    single-line
                    required
                  ></v-select>
                </v-flex>
                <v-flex xs8 sm4 offset-sm2>
                  <v-select
                    :items="productCosts.types"
                    v-model="damageReport.itemType"
                    label="Product Type"
                    single-line
                    required
                  ></v-select>
                </v-flex>
              </v-layout>
            </v-card-text>
          </v-card>
    <p><b>Current Damage Report</b>: {{ damageReport }}</p>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'AddDamages',
  data() {
    return {
      appData: {},
      productCosts: null,
      damageReasons: null,
      damageDept: null,
      damageReport: {}
    }
  },
  method: {
    addDamages() {}
  },
  created() {
    // Get damage reasons from firestore
    db
      .collection('appData')
      .doc('damageReasons')
      .get()
      .then(doc => {
        this.damageReasons = doc.data()
      })
      .catch(err => {
        console.log(err)
      })

    // Get product costs from firestore
    db
      .collection('appData')
      .doc('productCosts')
      .get()
      .then(doc => {
        this.productCosts = doc.data()
        this.productCosts.types = Object.keys(this.productCosts)
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style>
</style>
