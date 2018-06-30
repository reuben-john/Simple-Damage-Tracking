<template>
        <v-card>
          <v-card-text>
            <v-dialog v-model="editDialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="headline"> Edit Item </span>
                </v-card-title>
                <v-card-text>
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="item.name"
                          label="Category Name"
                          type="text"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="item.boxCost"
                          label="Box Cost"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="item.itemCost"
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
            <v-dialog v-model="addDialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <span class="headline"> Edit Item </span>
                </v-card-title>
                <v-card-text>
                  <v-container grid-list-md>
                    <v-layout wrap>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="item.name"
                          label="Category Name"
                          type="text"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="item.boxCost"
                          label="Box Cost"
                          type="number"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12 sm6 md4>
                        <v-text-field
                          v-model="item.itemCost"
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
          <v-card-actions>
            <v-layout row wrap justify-center>
              <v-flex>
                <v-btn color="success" @click="addItem">Add New Type</v-btn>
              </v-flex>
            </v-layout>
          </v-card-actions>
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
      editDialog: false,
      addDialog: false,
      editedIndex: -1,
      item: {
        name: '',
        boxCost: 0,
        itemCost: 0
      },
      defaultItem: {
        name: 'test',
        boxCost: 1,
        itemCost: 1
      }
    }
  },
  methods: {
    addItem(item) {
      this.editedIndex = this.productCosts.indexOf(item)
      this.item = Object.assign({}, item)
      this.addDialog = true
    },
    editItem(item) {
      this.editedIndex = this.productCosts.indexOf(item)
      this.item = Object.assign({}, item)
      this.editDialog = true
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
      // Convert name to lowercase as doc id is lowercase category name
      let id = item.name.toLowerCase()

      confirm('Are you sure you want to delete this item?') &&
        (this.productCosts.splice(index, 1), this.deleteFromDB(id))
    },
    close() {
      this.editDialog = false
      this.addDialog = false
      setTimeout(() => {
        this.item = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    save() {
      let id = this.item.name.toLowerCase()
      // Check if adding or updating item
      if (this.editedIndex > -1) {
        Object.assign(this.productCosts[this.editedIndex], this.item)
        // Convert name to lowercase as doc id is lowercase category name

        if (this.editDialog == true) {
          this.updateItem(id)
        }
      } else if (this.addDialog == true) {
        this.addNewItem(id)
      }
      this.close()
    },
    convertNumbers() {
      let report = Object.assign(this.item)

      // Convert string to numbers for different fields before adding to database
      report = Object.assign(report, {
        boxCost: parseFloat(report.boxCost),
        itemCost: parseFloat(report.itemCost)
      })
      return report
    },
    updateItem(itemId) {
      // Convert edited numbers to fields
      let report = Object.assign(this.item)
      this.item = this.convertNumbers(report)

      let ref = db.collection('productCosts').doc(itemId)
      // fetch data from firestore
      let querty = ref
        .update({
          name: this.item.name,
          boxCost: this.item.boxCost,
          itemCost: this.item.itemCost
        })
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    },
    addNewItem(itemId) {
      // Convert edited numbers to fields
      let report = Object.assign(this.item)
      this.item = this.convertNumbers(report)

      let ref = db.collection('productCosts').doc(itemId)
      // fetch data from firestore
      let querty = ref
        .set(this.item)
        .then(console.log('Added'))
        .catch(err => {
          console.log(err)
        })
    }
  },
  watch: {
    editDialog(val) {
      val || this.close()
    },
    addDialog(val) {
      val || this.close()
    }
  }
}
</script>

<style>
</style>
