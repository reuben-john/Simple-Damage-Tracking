// TODO Move order form to seperate vue template and load it in when needed.
// TODO Create warehouse form
// TODO Add form validation to validate numbers
// TODO Ensure all data that should be numbers gets converted before adding it to the d-block
// TODO Update the total damages tallies before returning to the Index page


<template>
  <div class="add-damages">
    <v-container text-xs-center>
      <v-layout row wrap align-center>
        <v-flex xs12 sm6 offset-sm1 offset-md2>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>Add Damage Report</h1>
              </v-flex>
            </v-card-title>
            <v-form>

              <v-card-text v-if="dataDownloaded">
                <h4>What type of damage do you wish to log?</h4>
                <v-radio-group
                v-model="damageReport.damageDept">
                  <v-layout row wrap>
                      <v-flex xs12 sm6
                      v-for="(reason, index) in damageReasons.reasons"
                      :key="index">
                        <v-radio
                          :key="reason"
                          :label="`${reason} damage report`"
                          :value="reason"
                        ></v-radio>
                      </v-flex>
                        <h2>{{damageDept}}</h2>
                      </v-layout>
                    </v-radio-group>
                  <v-layout v-if="damageReport.damageDept == 'order'">
                    <order-damages-form :damageReasons="damageReasons" :damageReport="damageReport" :productCosts="productCosts"></order-damages-form>
                </v-layout>
                <v-layout v-else-if="damageReport.damageDept == 'warehouse'">
                    <warehouse-damages-form :damageReasons="damageReasons" :damageReport="damageReport" :productCosts="productCosts"></warehouse-damages-form>
                </v-layout>
              </v-card-text>
              <v-btn v-if="dataDownloaded"
                @click="logDamages"
              >
              Log Damages
            </v-btn>
            </v-form>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import db from '@/firebase/init'
import OrderDamagesForm from '@/components/OrderDamagesForm'
import WarehouseDamagesForm from '@/components/WarehouseDamagesForm'

export default {
  name: 'AddDamages',
  components: {
    OrderDamagesForm,
    WarehouseDamagesForm
  },
  data() {
    return {
      appData: {},
      productCosts: null,
      damageReasons: null,
      damageDept: null,
      damageReport: {}
    }
  },
  methods: {
    logDamages() {
      // Add timestamp to report
      this.damageReport.timestamp = Date.now()

      // Pull product cost for a box loss if damage report is for bad box
      // Otherwise default to individual item cost
      if (this.damageReport.reasonLost == 'Bad Box') {
        this.damageReport.itemCost = this.productCosts[this.damageReport.itemType].boxCost
      } else {
        this.damageReport.itemCost = this.productCosts[this.damageReport.itemType].itemCost
      }

      let report = Object.assign(this.damageReport)
      this.damageReport = this.convertNumbers(report)

      // Send damage report to database
      db
        .collection('damages')
        .add(this.damageReport)
        .then(() => {
          this.$router.push({ name: 'Index' })
        })
        .catch(err => console.log(err))
    },
    convertNumbers(report) {
      // Convert string to numbers for different fields before adding to database
      if (report.damageDept == 'order') {
        report = Object.assign(report, {
          orderTotal: parseFloat(report.orderTotal),
          shippingCost: parseFloat(report.shippingCost),
          shippingLost: parseFloat(report.shippingLost),
          itemsLost: parseInt(report.itemsLost)
        })
      } else if (report.damageDept == 'warehouse') {
        report = Object.assign(report, {
          itemsLost: parseInt(report.itemsLost)
        })
      }
    },
    initialize() {
      // Get damage reasons from firestore
      db
        .collection('appData')
        .doc('damageReasons')
        .get()
        .then(doc => {
          this.damageReasons = doc.data()
          this.damageReasons.reasons = Object.keys(this.damageReasons)
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
  },
  created() {
    this.initialize()
  },
  computed: {
    dataDownloaded() {
      return this.damageReasons && this.productCosts
    }
  }
}
</script>

<style>
</style>
