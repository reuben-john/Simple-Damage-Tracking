<template>
  <v-container text-xs-center fill-height class="view-warehouse-damages">
      <v-layout row wrap align-center>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>Warehouse Damages</h1>
              </v-flex>
            </v-card-title>
            <v-card-text>
              <v-dialog v-model="dialog" max-width="500px" v-if="dataDownloaded">
                <v-card>
                  <v-card-title>
                    <span class="headline"> Edit Item </span>
                  </v-card-title>
                  <v-card-text>
                    <v-container grid-list-md>
                      <v-layout wrap>
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
                          <v-text-field v-model="editedItem.itemCost" label="Cost"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.itemsLost" label="Lost"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-select
                            :items="damageReasons.reasons"
                            v-model="editedItem.reasonLost"
                            label="Reason Lost"
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
                    <v-btn color="blue darken-1" flat @click.native="save">Save</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-data-table
              :headers="warehouseHeaders"
              :items="warehouseDamages"
              hide-actions
              class="elevation-1"
              >
                <template slot="items" slot-scope="props">
                  <td class="text-xs-left">{{ props.item.timestamp }}</td>
                  <td class="text-xs-left">{{ props.item.itemType }}</td>
                  <td class="text-xs-left">{{ props.item.itemCost }}</td>
                  <td class="text-xs-left">{{ props.item.itemsLost }}</td>
                  <td class="text-xs-left">{{ props.item.reasonLost }}</td>
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
  name: 'ViewWarehouseDamages',
  data() {
    return {
      // productCosts: null,
      productCosts: [],
      // damageReasons: null,
      damageReasons: null,
      costsLoaded: false,
      reasonsLoaded: false,
      warehouseDamages: [],
      warehouseHeaders: [
        { text: 'Date', value: 'timestamp' },
        { text: 'Item Type', value: 'itemType' },
        { text: 'Items Lost', value: 'itemsLost' },
        { text: 'Item Cost', value: 'itemCost' },
        { text: 'Reason Lost', value: 'reasonLost' }
      ],
      dialog: false,
      editedIndex: -1,
      editedItem: {
        itemType: '',
        itemsLost: 0,
        itemCost: 0,
        reasonLost: ''
      },
      defaultItem: {
        itemType: '',
        itemsLost: 0,
        itemCost: 0,
        reasonLost: ''
      }
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
  methods: {
    updateTally(tally) {
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
    tallyNewTotals() {
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
          this.updateTally(warehouseTally)
        })
        .catch(err => {
          console.log(err)
        })
    },
    initialize() {
      let damagesRef = db.collection('damages').orderBy('timestamp')
      // fetch data from firestore
      let query = damagesRef
        .where('damageDept', '==', 'warehouse')
        .get()
        .then(snapshot => {
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

      db
        .collection('damageReasons')
        .doc('warehouse')
        .get()
        .then(doc => {
          this.damageReasons = doc.data()
          this.reasonsLoaded = true
        })
        .catch(err => console.log(err))
    },
    editItem(item) {
      this.editedIndex = this.warehouseDamages.indexOf(item)
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
      const index = this.warehouseDamages.indexOf(item)
      let id = this.warehouseDamages[index].id
      confirm('Are you sure you want to delete this item?') &&
        (this.warehouseDamages.splice(index, 1), this.deleteFromDB(id))

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
        Object.assign(this.warehouseDamages[this.editedIndex], this.editedItem)
        let id = this.warehouseDamages[this.editedIndex].id
        this.updateItem(id)
      }
      this.close()
    },
    convertNumbers(report) {
      // Convert string to numbers for different fields before adding to database
      report = Object.assign(report, {
        itemsLost: parseInt(report.itemsLost),
        itemCost: parseFloat(report.itemCost)
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
          itemsLost: this.editedItem.itemsLost,
          itemCost: this.editedItem.itemCost,
          reasonLost: this.editedItem.reasonLost
        })
        .then(console.log('Updated'), this.tallyNewTotals())
        .catch(err => {
          console.log(err)
        })
    }
  },
  computed: {
    dataDownloaded() {
      return this.costsLoaded && this.reasonsLoaded
    }
  }
}
</script>

<style>
</style>
