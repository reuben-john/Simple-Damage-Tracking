<template>
        <v-card>
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
                        <v-text-field
                          v-model="editedItem.name"
                          label="Category Name"
                          type="text"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="editedItem.boxCost"
                          label="Box Cost"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="editedItem.itemCost"
                          label="Item Cost"
                          type="number"
                        ></v-text-field>
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
            <v-layout row wrap justify-space-around>
              <v-flex xs12 sm8 >
                <v-data-table
                  :headers="reasonHeaders"
                  :items="productCosts"
                  hide-actions
                  class="elevation-1"
                  >
                  <template slot="items" slot-scope="props">
                    <td class="text-xs-left">{{ props.item.name }}</td>
                    <td class="text-xs-left">${{ props.item.boxCost }}</td>
                    <td class="text-xs-left">${{ props.item.itemCost }}</td>
                    <td class="justify-center layout px-0">
                      <v-btn icon class="mx-0" @click="editItem(props.item)">
                        <v-icon color="teal">edit</v-icon>
                      </v-btn>
                      <v-btn icon class="mx-0" @click="deleteItem(props.item)">
                        <v-icon color="pink">delete</v-icon>
                      </v-btn>
                    </td>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>

</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'EditProductCosts',
  props: ['productCosts'],
  data() {
    return {
      reasonHeaders: [
        { text: 'Name', value: 'name' },
        { text: 'Box Cost', value: 'boxCost' },
        { text: 'Item Cost', value: 'itemCost' }
      ],
      dialog: false,
      editedIndex: -1,
      editedItem: {
        name: '',
        boxCost: 0,
        itemCost: 0
      },
      defaultItem: {
        name: '',
        boxCost: 0,
        itemCost: 0
      }
    }
  },
  methods: {
    editItem(item) {
      this.editedIndex = this.productCosts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteFromDB(itemId) {
      db
        .collection('productCosts')
        .doc(itemId)
        .delete()
        .then(console.log('Deleted'))
        .catch(err => console.log(err))
    },
    deleteItem(item) {
      const index = this.productCosts.indexOf(item)
      console.log(item)
      // Convert name to lowercase as doc id is lowercase category name
      let id = item.name.toLowerCase()
      console.log(id)

      confirm('Are you sure you want to delete this item?') &&
        (this.productCosts.splice(index, 1), this.deleteFromDB(id))
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
        Object.assign(this.productCosts[this.editedIndex], this.editedItem)
        // Convert name to lowercase as doc id is lowercase category name
        let id = item.name.toLowerCase()

        this.updateItem(id)
      }
      this.close()
    },
    convertNumbers() {
      let report = Object.assign(this.editedItem)

      // Convert string to numbers for different fields before adding to database
      report = Object.assign(report, {
        boxCost: parseFloat(report.boxCost),
        itemCost: parseFloat(report.itemCost)
      })
      return report
    },
    updateItem(itemId) {
      // Convert edited numbers to fields
      let report = Object.assign(this.editedItem)
      this.editedItem = this.convertNumbers(report)

      let ref = db.collection('productCosts').doc(itemId)
      // fetch data from firestore
      let querty = ref
        .update({
          name: this.editedItem.name,
          boxCost: this.editedItem.boxCost,
          itemCost: this.editedItem.itemCost
        })
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    }
  },
  watch: {
    dialog(val) {
      val || this.close()
    }
  }
}
</script>

<style>
</style>
