<template>
  <v-container class="add-damages" text-xs-center fluid fill-height>
    <loading v-if="loading"></loading>
    <v-layout row wrap align-center justify-center v-if="dataDownloaded">
      <v-flex xs12 sm6>
        <v-card class="elevation-12">
          <v-card-title primary-title>
            <v-flex>
              <h1>Add Damage Report</h1>
            </v-flex>
          </v-card-title>
          <v-card-text v-if="!reportLogged">
            <v-form @submit.prevent="logDamages">
              <h4>What type of damage do you wish to log?</h4>
              <v-radio-group v-model="damageReport.damageDept">
                <v-layout row wrap>
                  <v-flex
                    xs12
                    sm6
                    align-center
                    justify-center
                    v-for="(reason, index) in damageReasons"
                    :key="index"
                  >
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
                <order-damages-form
                  :damageReasons="damageReasons"
                  :damageReport="damageReport"
                  :productCosts="productCosts"
                  :ebayAccounts="ebayAccounts"
                ></order-damages-form>
              </v-layout>
              <v-layout v-else-if="damageReport.damageDept == 'warehouse'">
                <warehouse-damages-form
                  :damageReasons="damageReasons"
                  :damageReport="damageReport"
                  :productCosts="productCosts"
                ></warehouse-damages-form>
              </v-layout>
              <v-btn v-if="dataDownloaded" type="submit">Log Damages</v-btn>
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
import Loading from '@/components/layout/Loading'
import moment from 'moment'
import dbTools from '@/mixins/dbTools.js'

export default {
  name: 'AddDamages',
  mixins: [dbTools],
  components: {
    OrderDamagesForm,
    WarehouseDamagesForm,
    DamageReportThanks,
    Loading
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
      reportLogged: false,
      loading: true
    }
  },
  methods: {
    tallyNewTotals() {
      // Queries firestore for current damages and tallies total

      // Check whether adding order report or warehouse report
      if (this.damageReport.damageDept == 'order') {
        this.tallyNewOrderTotals()
      } else if (this.damageReport.damageDept == 'warehouse') {
        this.tallyNewWarehouseTotals()
      }
    },
    showReportLogged() {
      // Show thanks message
      this.reportLogged = true
      let vm = this
      setTimeout(function() {
        vm.$router.push({ name: 'Index' })
      }, 1000)
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
      db.collection('damages')
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
          report.returnLabel = false
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
      db.collection('damageReasons')
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
      db.collection('productCosts')
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
      db.collection('ebayAccounts')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.ebayAccounts.push(doc.data().ebayAccount)
          })

          // Displays loading graphic for 800ms before showing table
          let vm = this
          setTimeout(() => {
            this.loading = false
            this.accountsLoaded = true
          }, 400)
        })
        .catch(err => console.log(err))
    }
  },
  created() {
    // Display loading graphic during page load, closes it after last database call
    this.loading = true
    this.initialize()
  },
  computed: {
    dataDownloaded() {
      // Checks for each database call to be finished
      return this.damagesLoaded && this.costsLoaded && this.accountsLoaded
    }
  }
}
</script>

<style>
</style>
