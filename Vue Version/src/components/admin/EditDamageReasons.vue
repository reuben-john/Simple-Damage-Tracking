<template>

        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Damage Reasons</h2>
            </v-flex>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
                <v-layout row wrap align-center justify-center>
                  <v-flex xs12 sm6 md4>
                    <v-select
                      :items="damageReasons.departments"
                      v-model="department"
                      label="Choose Department"
                      single-line
                      required
                    ></v-select>
                  </v-flex>
                </v-layout>
                <v-layout align-center justify-center row wrap v-if="department == 'order'">
                  <v-flex xs12 sm6 md4>
                    <v-select
                      :items="damageReasons.order.reasons"
                      v-model="reason"
                      label="Damage Reason to Edit"
                      single-line
                      required
                    ></v-select>
                  </v-flex>
                  <v-flex xs12 sm6 md4>
                    <v-text-field
                      required v-model="updatedReason" label="Update Reason"></v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
          </v-card-text>
          <v-card-text>
            <v-layout row wrap justify-space-around>
              <v-flex xs12 sm5 >
                <v-data-table
                  :headers="reasonHeaders"
                  :items="tableFormated.order"
                  hide-actions
                  class="elevation-1"
                  >
                  <template slot="items" slot-scope="props">
                    <td class="text-xs-left">Order</td>
                    <td class="text-xs-left">{{ props.item.reasons }}</td>
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
              </v-flex>
              <v-flex xs12 sm5>
                <v-data-table
                  :headers="reasonHeaders"
                  :items="tableFormated.warehouse"
                  hide-actions
                  class="elevation-1"
                  >
                  <template slot="items" slot-scope="props">
                    <td class="text-xs-left">Warehouse</td>
                    <td class="text-xs-left">{{ props.item.reasons }}</td>
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
              </v-flex>
            </v-layout>

          </v-card-text>
          <v-card-actions>
            <v-layout wrap justify-center align-center>
              <v-flex xs12 >
                <v-btn v-if="updatedReason"
                  @click="updateReason"
                  >
                  Update
                </v-btn>
                <v-btn v-if="updatedReason"
                  @click="deleteReason"
                  >
                  Delete
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card-actions>
        </v-card>

</template>

<script>
import db from '@/firebase/init'

export default {
  name: 'EditDamageReasons',
  props: ['damageReasons'],
  data() {
    return {
      department: '',
      reason: '',
      updatedReason: '',
      reasonHeaders: [{ text: 'Department', value: 'department' }, { text: 'Reason', value: 'reasons' }],
      testReasons: [{ department: 'Order', reasons: 'Bad Product' }, { department: 'Warehouse', reasons: 'Bad Box' }],
      tableFormated: {
        order: [],
        warehouse: []
      }
    }
  },
  methods: {
    formatTableData() {
      let orderReasons = this.damageReasons.order.reasons
      let warehouseReasons = this.damageReasons.warehouse.reasons
      console.log(warehouseReasons)

      orderReasons.forEach(reason => {
        this.tableFormated.order.push({ department: this.damageReasons.order.department, reasons: reason })
      })

      warehouseReasons.forEach(reason => {
        this.tableFormated.warehouse.push({
          department: this.damageReasons.warehouse.department,
          reasons: reason
        })
      })
    },
    updateReason() {
      let reasons = this.damageReasons[this.department].reasons
      let index = reasons.indexOf(this.reason)
      reasons[index] = this.updatedReason
      this.damageReasons[this.department].reasons = reasons

      // update database
      db
        .collection('damageReasons')
        .doc(this.department)
        .set(
          {
            test: reasons
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => console.log)
    },
    deleteReason() {
      let reasons = this.damageReasons.order.reasons
      let index = reasons.indexOf(this.reason)
      reasons.splice(index, 1)
      this.damageReasons.order.reasons = reasons

      // update database
      db
        .collection('damageReasons')
        .doc(this.department)
        .set(
          {
            test: reasons
          },
          { merge: true }
        )
        .then(console.log('Deleted'))
        .catch(err => console.log)
    },
    deleteItem() {},
    editItem() {},
    initialize() {}
  },
  computed: {
    orderReasons() {
      return this.damageReasons.order.reasons
    }
  },
  created() {
    this.formatTableData()
  }
}
</script>

<style>
</style>
