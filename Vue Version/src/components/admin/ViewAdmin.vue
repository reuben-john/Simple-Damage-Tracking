<template>
  <v-container class="view-admin" text-xs-center fill-height>
    <v-layout row wrap align-center justify-center>
      <loading v-if="loading"></loading>
      <v-flex xs12 sm10 v-if="accountsLoaded">
        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Admin Options</h2>
            </v-flex>
          </v-card-title>
          <v-card-text>
            <v-layout row wrap justify-center align-center>
              <v-flex xs2>
                <v-btn
                  color="purple darken-1 white--text"
                  @click="editReasons = !editReasons"
                >Edit Damage Reasons</v-btn>
              </v-flex>
              <v-flex xs2>
                <v-btn
                  color="purple darken-1 white--text"
                  @click="editCosts = !editCosts"
                >Edit Product Costs</v-btn>
              </v-flex>
              <v-flex xs2>
                <v-btn
                  color="purple darken-1 white--text"
                  @click="editAccounts = !editAccounts"
                >Edit Ebay Accounts</v-btn>
              </v-flex>
              <v-flex xs2>
                <v-btn
                  color="purple darken-1 white--text"
                  @click="downloadDamages = !downloadDamages"
                >Download Damage Report</v-btn>
              </v-flex>
              <v-flex xs2>
                <v-btn
                  color="purple darken-1 white--text"
                  @click="uploadCsv = !uploadCsv"
                >Upload CSV Data</v-btn>
              </v-flex>
              <v-flex xs3>
                <v-btn
                  color="purple darken-1 white--text"
                  @click="uploadEbayInventory = !uploadEbayInventory"
                >Ebay Inventory Tools</v-btn>
              </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-text>
            <edit-damage-reasons v-if="editReasons" :damageReasons="damageReasons"></edit-damage-reasons>
            <edit-product-costs v-if="editCosts" :productCosts="productCosts"></edit-product-costs>
            <edit-ebay-accounts v-if="editAccounts" :ebayAccounts="ebayAccounts"></edit-ebay-accounts>
            <upload-csv v-if="uploadCsv" :damageReasons="damageReasons"></upload-csv>
            <upload-ebay-inventory v-if="uploadEbayInventory"></upload-ebay-inventory>
            <download-damages-form v-if="downloadDamages" :years="years"></download-damages-form>
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
import DownloadDamagesForm from '@/components/admin/DownloadDamagesForm'
import Loading from '@/components/layout/Loading'
import UploadCsv from '@/components/admin/UploadCsv'
import db from '@/firebase/init'
import jsPDF from 'jspdf'
import dbTools from '@/mixins/dbTools.js'
import UploadEbayInventory from '@/components/admin/UploadEbayInventory'

export default {
  name: 'ViewAdmin',
  mixins: [dbTools],
  components: {
    EditProductCosts,
    EditDamageReasons,
    EditEbayAccounts,
    UploadCsv,
    UploadEbayInventory,
    Loading,
    DownloadDamagesForm
  },
  data() {
    return {
      // Used to show or hide different parts of the app
      editReasons: false,
      editCosts: false,
      editAccounts: false,
      uploadCsv: false,
      uploadEbayInventory: false,
      loading: true,
      accountsLoaded: false,
      downloadDamages: false,

      // Data holders
      ebayAccounts: {
        accounts: null
      },
      damageReasons: {},
      productCosts: []
    }
  },

  created() {
    // Display loading graphic during page load, closes it after last database call
    this.loading = true
    this.fetchYears()
    // fetch product costs from firestore
    db.collection('productCosts')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.productCosts.push(doc.data())
        })
      })
      .catch(err => console.log(err))

    // Fetch damage reasons from firestore
    this.damageReasons.departments = []
    db.collection('damageReasons')
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
    db.collection('ebayAccounts')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.ebayAccounts[doc.id] = doc.data()
          this.ebayAccounts.accounts.push(doc.data().ebayAccount)
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
}
</script>
