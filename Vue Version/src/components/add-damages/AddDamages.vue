<template>
    <v-container class="add-damages" text-xs-center fluid fill-height>
      <v-layout row wrap align-center justify-center>
        <v-flex xs12 sm6>
          <v-card class="elevation-12">
            <v-card-title primary-title>
              <v-flex>
                <h1>Add Damage Report</h1>
              </v-flex>
            </v-card-title>
            <v-card-text v-if="!reportLogged">
              <v-form v-if="dataDownloaded" @submit.prevent="logDamages">
                <h4>What type of damage do you wish to log?</h4>
                <v-radio-group
                v-model="damageReport.damageDept" >
                  <v-layout row wrap >
                      <v-flex xs12 sm6 align-center justify-center
                      v-for="(reason, index) in damageReasons"
                      :key="index">
                        <v-radio
                          :key="reason.department"
                          :label="`${reason.department} damage report`"
                          :value="reason.id"
                        ></v-radio>
                      </v-flex>
                        <h2>{{damageDept}}</h2>
                      </v-layout>
                    </v-radio-group>
                  <v-layout v-if="damageReport.damageDept == 'order'">
                    <order-damages-form :damageReasons="damageReasons" :damageReport="damageReport" :productCosts="productCosts" :ebayAccounts="ebayAccounts"></order-damages-form>
                </v-layout>
                <v-layout v-else-if="damageReport.damageDept == 'warehouse'">
                    <warehouse-damages-form :damageReasons="damageReasons" :damageReport="damageReport" :productCosts="productCosts"></warehouse-damages-form>
                </v-layout>
                <v-btn v-if="dataDownloaded"
                  type="submit"
                  >
                  Log Damages
                </v-btn>
              </v-form>
            </v-card-text>
            <v-card-text v-if="reportLogged">
              <damage-report-thanks></damage-report-thanks>
            </v-card-text>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import db from '@/firebase/init'
import OrderDamagesForm from '@/components/add-damages/OrderDamagesForm'
import WarehouseDamagesForm from '@/components/add-damages/WarehouseDamagesForm'
import DamageReportThanks from '@/components/add-damages/DamageReportThanks'

export default {
  name: 'AddDamages',
  components: {
    OrderDamagesForm,
    WarehouseDamagesForm,
    DamageReportThanks
  },
  data() {
    return {
      productCosts: {},
      damageReasons: {},
      damageDept: null,
      damageReport: {},
      costsLoaded: false,
      damagesLoaded: false,
      ebayAccounts: null,
      accountsLoaded: false,
      reportLogged: false
    }
  },
  methods: {
    tallyNewTotals() {
      if (this.damageReport.damageDept == 'order') {
        this.tallyNewOrderTotals()
      } else if (this.damageReport.damageDept == 'warehouse') {
        this.tallyNewWarehouseTotals()
      }
    },
    updateOrderTally(orderTally, shippingTally) {
      // fetch data from firestore
      db
        .collection('totalLosses')
        .doc('order')
        .set(
          {
            total: parseFloat((orderTally + shippingTally).toFixed(2)),
            itemTotal: orderTally,
            shipTotal: shippingTally
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    },
    tallyNewOrderTotals() {
      let damagesRef = db.collection('damages')
      let orderTally = 0
      let shippingTally = 0

      // Tally order totals
      let orderQuery = damagesRef
        .where('damageDept', '==', 'order')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let cost = doc.data().itemCost
            let numLost = doc.data().itemsLost
            let shipCost = doc.data().shippingCost
            let shipLost = doc.data().shippingLost
            let returnCost = 0
            if (doc.data().returnCost) {
              returnCost = doc.data().returnCost
            }
            shippingTally += shipLost + returnCost
            orderTally += cost * numLost
          })
          // Normalize cost to 2 decimal places so it is accurate for money display $xx.xx
          orderTally = parseFloat(orderTally.toFixed(2))
          shippingTally = parseFloat(shippingTally.toFixed(2))
          this.updateOrderTally(orderTally, shippingTally)
        })
        .catch(err => {
          console.log(err)
        })
    },
    updateWarehouseTally(tally) {
      // fetch data from firestore
      db
        .collection('totalLosses')
        .doc('warehouse')
        .set(
          {
            total: tally
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    },
    tallyNewWarehouseTotals() {
      let damagesRef = db.collection('damages')
      let warehouseTally = 0
      // Tally warehouse totals
      let warehouseQuery = damagesRef
        .where('damageDept', '==', 'warehouse')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let cost = doc.data().itemCost
            let numLost = doc.data().itemsLost
            warehouseTally += cost * numLost
          })
          // Normalize cost to 2 decimal places so it is accurate for money display $xx.xx
          warehouseTally = parseFloat(warehouseTally.toFixed(2))
          this.updateWarehouseTally(warehouseTally)
        })
        .catch(err => {
          console.log(err)
        })
    },
    showReportLogged() {
      // Show thanks message
      this.reportLogged = true
      let vm = this
      setTimeout(function() {
        vm.$router.push({ name: 'Index' })
      }, 2000)
    },
    logDamages() {
      // Add timestamp to report
      this.damageReport.timestamp = Date.now()

      // Convert itemType to lowercase to allow product costs to pull the correct numbers
      let itemType = this.damageReport.itemType
      this.damageReport.itemType = itemType.toLowerCase()

      // Pull product cost for a box loss if damage report is for bad box
      // Otherwise default to individual item cost
      if (this.damageReport.reasonLost == 'Bad Box') {
        this.damageReport.itemCost = this.productCosts[this.damageReport.itemType].boxCost
      } else {
        this.damageReport.itemCost = this.productCosts[this.damageReport.itemType].itemCost
      }

      let report = Object.assign(this.damageReport)
      this.damageReport = this.convertNumbers(report)

      let vm = this
      // Send damage report to database
      db
        .collection('damages')
        .add(this.damageReport)
        .then(() => {
          this.showReportLogged()
        })
        .catch(err => console.log(err))
      this.tallyNewTotals()
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
        if (report.returnLabel) {
          report.returnCost = parseFloat(report.returnCost)
        } else {
          report.returnCost = 0
        }
      } else if (report.damageDept == 'warehouse') {
        report = Object.assign(report, {
          itemsLost: parseInt(report.itemsLost)
        })
      }
      return report
    },
    initialize() {
      // Get damage reasons from firestore
      db
        .collection('damageReasons')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let report = doc.data()
            report.id = doc.id
            this.damageReasons[doc.id] = report
          })
          this.damagesLoaded = true
        })
        .catch(err => console.log(err))

      // Get product costs from firestore
      this.productCosts.types = []
      db
        .collection('productCosts')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let report = doc.data()
            report.id = doc.id
            this.productCosts[doc.id] = report
            this.productCosts.types.push(doc.data().name)
          })
          this.costsLoaded = true
        })
        .catch(err => console.log(err))
      // Get ebay account names from firestore
      this.ebayAccounts = []
      db
        .collection('ebayAccounts')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.ebayAccounts.push(doc.data().ebayAccount)
          })
          this.accountsLoaded = true
        })
        .catch(err => console.log(err))
    }
  },
  created() {
    this.initialize()
  },
  computed: {
    dataDownloaded() {
      return this.damagesLoaded && this.costsLoaded && this.accountsLoaded
    }
  }
}
</script>

<style>
</style>
