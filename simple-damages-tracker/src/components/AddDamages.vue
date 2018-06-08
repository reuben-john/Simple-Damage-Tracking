<template>
  <div class="add-damages">
    <v-container>
      <v-layout row wrap>
      <v-flex xs12 sm6 offset-sm3>
        <v-card width="600">
          <v-card-title primary-title>
            <v-flex text-xs-center>Add Damage</v-flex>
          </v-card-title>
          <v-card-text v-if="damageReasons">
            <v-select
          :items="orders"
          v-model="selected"
          label="Select"
          single-line
        ></v-select>
        <h2>{{ selected }}</h2>
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
  name: 'AddDamages',
  data() {
    return {
      departments: null,
      damageReasons: null,
      damageDept: null,
      selected: null,
      warehouse: ['Bad Product', 'Bad Box'],
      orders: ['Bad Product', 'Returned Product', 'Damaged in shipping']
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
