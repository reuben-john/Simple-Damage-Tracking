<template>
<div class="view-warehouse-damages">

  <v-container text-xs-center>
      <v-layout row wrap align-center>
        <v-flex>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>View warehouse Damages</h1>
              </v-flex>
            </v-card-title>
            <v-card-text>
              <v-dialog v-model="dialog" max-width="500px">
                <v-card>
                  <v-card-title>
                    <span class="headline"> Edit Item </span>
                  </v-card-title>
                  <v-card-text>
                    <v-container grid-list-md>
                      <v-layout wrap>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.itemType" label="Type"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.itemCost" label="Cost"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.itemsLost" label="Lost"></v-text-field>
                        </v-flex>
                        <v-flex xs12 sm6 md4>
                          <v-text-field v-model="editedItem.reasonLost" label="Reason"></v-text-field>
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
                  <td class="text-xs-left">{{ props.item.itemsLost }}</td>
                  <td class="text-xs-left">{{ props.item.itemCost }}</td>
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
</div>
</template>

<script>
import db from '@/firebase/init'
import moment from 'moment'

export default {
  name: 'ViewWarehouseDamages',
  data() {
    return {
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
        reasonLost: 0
      },
      defaultItem: {
        itemType: '',
        itemsLost: 0,
        itemCost: 0,
        reasonLost: 0
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
    initialize() {
      let damagesRef = db.collection('damages').orderBy('timestamp')
      // fetch data from firestore
      let querty = damagesRef
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
    },
    editItem(item) {
      this.editedIndex = this.warehouseDamages.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem(item) {
      const index = this.warehouseDamages.indexOf(item)
      confirm('Are you sure you want to delete this item?') && this.warehouseDamages.splice(index, 1)
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
    updateItem(itemId) {
      let damagesRef = db.collection('damages').doc(itemId)
      // fetch data from firestore
      let querty = damagesRef
        .update({
          itemsLost: this.editedItem.itemsLost,
          itemCost: this.editedItem.itemCost,
          reasonLost: this.editedItem.reasonLost
        })
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>
</style>
