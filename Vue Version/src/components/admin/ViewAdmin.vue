<template>
  <v-container class="view-admin" text-xs-center fill-height>
    <v-layout row wrap align-center justify-center>
      <v-flex xs12 sm10>
        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Admin Options</h2>
            </v-flex>
          </v-card-title>
          <v-card-text>
            <v-layout row wrap justify-center align-center>
            <v-flex xs2>
              <v-btn color="purple darken-1 white--text" @click="editReasons = !editReasons">Edit Damage Reasons</v-btn>
            </v-flex>
            <v-flex xs2>
              <v-btn color="purple darken-1 white--text" @click="editCosts = !editCosts">Edit Product Costs</v-btn>
            </v-flex>
            <v-flex xs2>
              <v-btn color="purple darken-1 white--text" @click="editAccounts = !editAccounts">Edit Ebay Accounts</v-btn>
            </v-flex>
            <v-flex xs2>
              <v-btn color="purple darken-1 white--text" @click="downloadCSV()">Download Damage Report</v-btn>
            </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-text>
            <edit-damage-reasons v-if="editReasons" :damageReasons="damageReasons"></edit-damage-reasons>
            <edit-product-costs v-if="editCosts" :productCosts="productCosts"></edit-product-costs>
            <edit-ebay-accounts v-if="editAccounts" :ebayAccounts="ebayAccounts"></edit-ebay-accounts>
          </v-card-text>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import EditDamageReasons from '@/components/admin/EditDamageReasons'
import EditProductCosts from '@/components/admin/EditProductCosts'
import EditEbayAccounts from '@/components/admin/EditEbayAccounts'
import db from '@/firebase/init'
import papaparse from 'papaparse'

export default {
  name: 'ViewAdmin',
  components: {
    EditProductCosts,
    EditDamageReasons,
    EditEbayAccounts
  },
  data() {
    return {
      editReasons: false,
      editCosts: false,
      editAccounts: false,
      ebayAccounts: {
        accounts: null
      },
      damageReasons: {},
      productCosts: [],
      CSVReport: null
    }
  },
  methods: {
    downloadCSV() {
      // Clears CSVreport
      this.CSVReport = []
      // fetch damages data from firestore
      db
        .collection('damages')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.CSVReport.push(doc.data())
          })
          // saves firestore data as csv - Must be inside [] for file-saver to work
          let csv = [papaparse.unparse(this.CSVReport, { download: true })]
          var FileSaver = require('file-saver')
          var blob = new Blob(csv, { type: 'text/plain;charset=utf-8' })
          FileSaver.saveAs(blob, 'damages.csv')
        })
        .catch(err => console.log(err))
    }
  },
  created() {
    // fetch data from firestore
    db
      .collection('productCosts')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.productCosts.push(doc.data())
        })
      })
      .catch(err => console.log(err))

    this.damageReasons.departments = []
    db
      .collection('damageReasons')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.damageReasons[doc.id] = doc.data()
          this.damageReasons.departments.push(doc.id)
        })
      })
      .catch(err => console.log(err))

    // Get ebay account names from firestore
    this.ebayAccounts.accounts = []
    db
      .collection('ebayAccounts')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.ebayAccounts[doc.id] = doc.data()
          this.ebayAccounts.accounts.push(doc.data().ebayAccount)
        })
        this.accountsLoaded = true
        console.log(this.ebayAccounts)
      })
      .catch(err => console.log(err))
  }
}
</script>
