<template>
  <v-container text-xs-center fill-height class="view-order-damages">
      <v-layout row wrap align-center>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>Order Damages</h1>
              </v-flex>
            </v-card-title>
            <v-dialog v-model="dialog" max-width="500px" v-if="dataDownloaded">
              <v-card>
                <v-form @submit.prevent="save">
                  <v-card-title>
                    <span class="headline"> Edit Item </span>
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
                          <v-text-field
                            v-model="editedItem.itemCost"
                            label="Item Cost"
                            type="number"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field
                            v-model="editedItem.itemsLost"
                            label="Items Lost"
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
              <v-data-table
              :headers="orderHeaders"
              :items="orderDamages"
              :search="search"
              :custom-filter="customFilter"
              :pagination.sync="pagination"
              class="elevation-1"
              >
                <template slot="items" slot-scope="props">
                  <td class="text-xs-left">{{ props.item.date }}</td>
                  <td class="text-xs-left">{{ props.item.orderNumber }}</td>
                  <td class="text-xs-left">${{ props.item.orderTotal }}</td>
                  <td class="text-xs-left">${{ props.item.shippingCost }}</td>
                  <td class="text-xs-left">${{ props.item.shippingLost }}</td>
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
                <template slot="footer">
                  <td colspan="100%">
                    <v-flex xs6 sm1>
                      <v-select
                      label="Year"
                      :items="damageYears"
                      v-model="search"
                    ></v-select>
                    </v-flex>
                  </td>
                </template>
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

export default {
  name: 'ViewOrderDamages',
  data() {
    return {
      pagination: {
        sortBy: 'timestamp',
        descending: true
      },
      productCosts: [],
      damageReasons: null,
      costsLoaded: false,
      reasonsLoaded: false,
      orderDamages: null,
      ebayAccounts: null,
      accountsLoaded: false,
      damageYears: [],
      orderHeaders: [
        { text: 'Date', value: 'timestamp' },
        { text: 'Ebay Order', value: 'orderNumber' },
        { text: 'Order Total', value: 'orderTotal' },
        { text: 'Shipping Cost', value: 'shippingCost' },
        { text: 'Shipping Lost', value: 'shippingLost' },
        { text: 'Item Type', value: 'itemType' },
        { text: 'Items Lost', value: 'itemsLost' },
        { text: 'Reason Lost', value: 'reasonLost' },
        { text: 'eBay Account', value: 'ebayAccount' }
      ],
      dialog: false,
      editedIndex: -1,
      editedItem: {
        orderNumber: 0,
        orderTotal: 0,
        shippingCost: 0,
        shippingLost: 0,
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
        itemType: '',
        itemsLost: 0,
        itemCost: 0,
        reasonLost: '',
        ebayAccount: ''
      },
      search: ''
    }
  },
  methods: {
    customFilter(items, search, filter) {
      search = search.toString().toLowerCase()
      return items.filter(row => filter(row['date'], search))
    },
    removeDuplicates(arr) {
      let uniqueArr = Array.from(new Set(arr))
      return uniqueArr
    },
    updateTally(orderTally, shippingTally) {
      // fetch data from firestore
      db
        .collection('totalLosses')
        .doc('order')
        .set(
          {
            total: orderTally + shippingTally,
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
    tallyNewTotals() {
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
            shippingTally += shipLost
            orderTally += cost * numLost
          })
          console.log(orderTally, shippingTally)
          this.updateTally(orderTally, shippingTally)
        })
        .catch(err => {
          console.log(err)
        })
    },
    initialize() {
      let damagesRef = db.collection('damages')
      // fetch data from firestore
      let querty = damagesRef
        .where('damageDept', '==', 'order')
        .get()
        .then(snapshot => {
          // Make orderDamages an object to add the damage reports to it
          this.orderDamages = []

          snapshot.forEach(doc => {
            let report = doc.data()
            report.id = doc.id
            report.value = false
            report.date = moment(report.timestamp).format('LL')
            this.orderDamages.push(report)
            this.damageYears.push(moment(report.timestamp).format('GGGG'))
          })
          this.damageYears = this.removeDuplicates(this.damageYears)
        })
        .catch(err => {
          console.log(err)
        })

      // Get product costs from firestore
      db
        .collection('productCosts')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            this.productCosts.push(doc.id)
          })
          this.costsLoaded = true
        })
        .catch(err => console.log(err))

      // Get damage reasons from firestore
      db
        .collection('damageReasons')
        .doc('order')
        .get()
        .then(doc => {
          this.damageReasons = doc.data()
          this.reasonsLoaded = true
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
    },
    editItem(item) {
      this.editedIndex = this.orderDamages.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteFromDB(itemId) {
      let damagesRef = db.collection('damages').doc(itemId)
      // fetch data from firestore
      let querty = damagesRef
        .delete()
        .then(console.log('Deleted'))
        .catch(err => {
          console.log(err)
        })
    },
    deleteItem(item) {
      const index = this.orderDamages.indexOf(item)
      let id = this.orderDamages[index].id
      confirm('Are you sure you want to delete this item?') &&
        (this.orderDamages.splice(index, 1), this.deleteFromDB(id))

      this.tallyNewTotals()
    },
    close() {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.orderDamages[this.editedIndex], this.editedItem)
        let id = this.orderDamages[this.editedIndex].id
        this.updateItem(id)
      }
      this.close()
    },
    convertNumbers() {
      let report = Object.assign(this.editedItem)

      // Convert string to numbers for different fields before adding to database
      report = Object.assign(report, {
        orderTotal: parseFloat(report.orderTotal),
        shippingCost: parseFloat(report.shippingCost),
        shippingLost: parseFloat(report.shippingLost),
        itemCost: parseFloat(report.itemCost),
        itemsLost: parseInt(report.itemsLost)
      })
      return report
    },
    updateItem(itemId) {
      // Convert edited numbers to fields
      let report = Object.assign(this.editedItem)
      this.editedItem = this.convertNumbers(report)

      let damagesRef = db.collection('damages').doc(itemId)
      // fetch data from firestore
      let querty = damagesRef
        .update({
          orderNumber: this.editedItem.orderNumber,
          orderTotal: this.editedItem.orderTotal,
          shippingCost: this.editedItem.shippingCost,
          shippingLost: this.editedItem.shippingLost,
          itemType: this.editedItem.itemType,
          itemsLost: this.editedItem.itemsLost,
          itemCost: this.editedItem.itemCost,
          reasonLost: this.editedItem.reasonLost,
          ebayAccount: this.editedItem.ebayAccount
        })
        .then(console.log('Updated'), this.tallyNewTotals())
        .catch(err => {
          console.log(err)
        })
    }
  },
  watch: {
    dialog(val) {
      val || this.close()
    }
  },
  created() {
    this.initialize()
  },
  computed: {
    dataDownloaded() {
      return this.costsLoaded && this.reasonsLoaded && this.accountsLoaded
    }
  }
}
</script>

<style>
</style>
