<template>
        <v-card>
          <v-card-text>
            <v-layout row wrap justify-space-around>
              <v-flex xs12 sm8 >
                <v-data-table
                  :headers="reasonHeaders"
                  :items="testReasons"
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
                  <template slot="no-data">
                    <v-btn color="primary" @click="initialize">Reset</v-btn>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>

</template>

<script>
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
      testReasons: [{ name: 'General', boxCost: 25, itemCost: 1 }, { name: 'Makeup', boxCost: 40, itemCost: 0.25 }]
    }
  },
  methods: {
    initialize() {},
    edit() {},
    delete() {}
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
  }
}
</script>

<style>
</style>
