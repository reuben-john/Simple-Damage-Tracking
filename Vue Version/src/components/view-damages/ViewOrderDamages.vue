<template>
  <v-container text-xs-center fill-height class="view-order-damages">
    <loading v-if="loading"></loading>
    <v-layout row wrap align-center v-if="dataDownloaded">
      <v-flex>
        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h1>Order Damages</h1>
            </v-flex>
          </v-card-title>
          <v-dialog v-model="dialog" max-width="500px">
            <v-card>
              <v-form @submit.prevent="save">
                <v-card-title>
                  <span class="headline">Edit Item</span>
                </v-card-title>
                <v-card-text>
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="editedItem.orderNumber"
                          label="Order Number"
                          type="text"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="editedItem.orderTotal"
                          label="Order Total"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="editedItem.shippingCost"
                          label="Shipping Cost"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="editedItem.shippingLost"
                          label="Shipping Lost"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-select
                          :items="productCosts"
                          v-model="editedItem.itemType"
                          label="Product Type"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.itemCost" label="Item Cost" type="number"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field v-model="editedItem.itemsLost" label="# Lost" type="number"></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-checkbox label="Return Label" v-model="editedItem.returnLabel"></v-checkbox>
                      </v-flex>
                      <v-flex xs12 sm6 md4 v-if="editedItem.returnLabel">
                        <v-text-field
                          v-model="editedItem.returnCost"
                          label="Return Label Cost"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6>
                        <v-select
                          :items="damageReasons.reasons"
                          v-model="editedItem.reasonLost"
                          label="Reason Lost"
                          type="text"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm6>
                        <v-select
                          :items="ebayAccounts"
                          v-model="editedItem.ebayAccount"
                          label="eBay Account"
                          type="text"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" flat @click.native="close">Cancel</v-btn>
                  <v-btn color="blue darken-1" flat type="submit">Save</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>
          <v-card-text v-if="orderDamages">
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-data-table
              :headers="orderHeaders"
              :items="orderDamages"
              :search="search"
              :pagination.sync="pagination"
              :rows-per-page-items="rows"
              class="elevation-1"
            >
              <template slot="items" slot-scope="props">
                <td class="text-xs-left">{{ props.item.date }}</td>
                <td class="text-xs-left">{{ props.item.orderNumber }}</td>
                <td class="text-xs-left">${{ props.item.orderTotal }}</td>
                <td class="text-xs-left">${{ props.item.shippingCost }}</td>
                <td class="text-xs-left">${{ props.item.shippingLost }}</td>
                <td class="text-xs-left">${{ props.item.returnCost }}</td>
                <td class="text-xs-left">{{ props.item.itemType }}</td>
                <td class="text-xs-left">{{ props.item.itemsLost }}</td>
                <td class="text-xs-left">{{ props.item.reasonLost }}</td>
                <td class="text-xs-left">{{ props.item.ebayAccount }}</td>
                <td class="justify-center layout px-0">
                  <v-btn icon class="mx-0" @click="editItem(props.item)">
                    <v-icon color="teal">edit</v-icon>
                  </v-btn>
                  <v-btn icon class="mx-0" @click="deleteItem(props.item)">
                    <v-icon color="pink">delete</v-icon>
                  </v-btn>
                </td>
              </template>
              <template slot="no-data">
                <v-btn color="primary" @click="initialize">Reset</v-btn>
              </template>
              <v-alert
                slot="no-results"
                :value="true"
                color="error"
                icon="warning"
              >Your search for "{{ search }}" found no results.</v-alert>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import db from '@/firebase/init'
import moment from 'moment'
import Loading from '@/components/layout/Loading'
import dbTools from '@/mixins/dbTools.js'

export default {
  name: 'ViewOrderDamages',
  mixins: [dbTools],
  components: {
    Loading
  },
  data() {
    return {
      // Table settings
      // Sets default table view to pages and default sort by timestamp
      pagination: {
        sortBy: 'timestamp',
        descending: true
      },
      // Number of rows to show and options to show more
      rows: [10, 25, { text: 'All', value: -1 }],
      // Table Headers
      orderHeaders: [
        { text: 'Date', value: 'date' },
        { text: 'Ebay Order', value: 'orderNumber' },
        { text: 'Order Total', value: 'orderTotal' },
        { text: 'Shipping Cost', value: 'shippingCost' },
        { text: 'Shipping Lost', value: 'shippingLost' },
        { text: 'Return Label Cost', value: 'returnCost' },
        { text: 'Item Type', value: 'itemType' },
        { text: '# Lost', value: 'itemsLost' },
        { text: 'Reason Lost', value: 'reasonLost' },
        { text: 'eBay Account', value: 'ebayAccount' }
      ],

      // Database info gets added to these items
      productCosts: [],
      damageReasons: null,
      orderDamages: null,
      ebayAccounts: null,

      // Used to show/hide page sections during page render

      // Settings for edit item card
      dialog: false,
      editedIndex: -1,
      editedItem: {
        orderNumber: 0,
        orderTotal: 0,
        shippingCost: 0,
        shippingLost: 0,
        returnLabel: false,
        returnCost: 0,
        itemType: '',
        itemsLost: 0,
        itemCost: 0,
        reasonLost: '',
        ebayAccount: ''
      },
      defaultItem: {
        orderNumber: 0,
        orderTotal: 0,
        shippingCost: 0,
        shippingLost: 0,
        returnLabel: false,
        returnCost: 0,
        itemType: '',
        itemsLost: 0,
        itemCost: 0,
        reasonLost: '',
        ebayAccount: ''
      },

      // Search by Year
      search: ''
    }
  },
  watch: {
    dialog(val) {
      // Watches for closing the dialog window
      val || this.close()
    }
  },
  created() {
    // Display loading graphic during page load, closes it after last database call
    this.loading = true
    this.loaded = false
    this.initialize()
  },
  computed: {
    dataDownloaded() {
      // Checks for each database call to be finished
      return this.costsLoaded && this.reasonsLoaded && this.accountsLoaded && this.loaded
    }
  },
  methods: {
    initialize() {
      let dept = 'order'
      this.orderDamages = this.fetchDamages(dept)
      this.productCosts = this.fetchProductCosts()
      this.damageReasons = this.fetchDamageReasons(dept)
      this.ebayAccounts = this.fetchEbayAccounts()
      this.displayLoading(800)
    },
    editItem(item) {
      // copies selected item info into temp holder to make changes to
      this.editedIndex = this.orderDamages.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem(item) {
      // Confirms you want to delete item, then deletes item

      const index = this.orderDamages.indexOf(item)
      let id = this.orderDamages[index].id
      confirm('Are you sure you want to delete this item?') &&
        (this.orderDamages.splice(index, 1), this.deleteFromDB(id))

      this.tallyNewOrderTotals()
    },
    close() {
      // Closes dialog window and resets editedItem to default settings

      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    save() {
      // Saves changes made in dialog window

      if (this.editedIndex > -1) {
        Object.assign(this.orderDamages[this.editedIndex], this.editedItem)
        let id = this.orderDamages[this.editedIndex].id
        this.updateItem(id)
      }
      this.close()
    },
    convertNumbers() {
      // Convert string to numbers for different fields before adding to database

      let report = Object.assign(this.editedItem)

      report = Object.assign(report, {
        orderTotal: parseFloat(report.orderTotal),
        shippingCost: parseFloat(report.shippingCost),
        shippingLost: parseFloat(report.shippingLost),
        itemCost: parseFloat(report.itemCost),
        itemsLost: parseInt(report.itemsLost)
      })
      if (report.returnLabel) {
        report.returnCost = parseFloat(report.returnCost)
      } else {
        report.returnCost = 0
      }
      return report
    },
    updateItem(itemId) {
      // Update edited item in firestore

      // Convert edited numbers to fields
      let report = Object.assign(this.editedItem)
      this.editedItem = this.convertNumbers(report)

      let damagesRef = db.collection('damages').doc(itemId)
      // Updates firestore doc
      let query = damagesRef
        .update({
          orderNumber: this.editedItem.orderNumber,
          orderTotal: this.editedItem.orderTotal,
          shippingCost: this.editedItem.shippingCost,
          shippingLost: this.editedItem.shippingLost,
          returnLabel: this.editedItem.returnLabel,
          returnCost: this.editedItem.returnCost,
          itemType: this.editedItem.itemType,
          itemsLost: this.editedItem.itemsLost,
          itemCost: this.editedItem.itemCost,
          reasonLost: this.editedItem.reasonLost,
          ebayAccount: this.editedItem.ebayAccount
        })
        .then(console.log('Updated'), this.tallyNewOrderTotals())
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>
</style>
