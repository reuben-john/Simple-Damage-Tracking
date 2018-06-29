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
      updatedReason: ''
    }
  },
  methods: {
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
