<template>
  <v-layout column>
    <v-flex xs12 sm6>
      <v-card>
        <v-container fluid grid-list-md>
          <v-layout row wrap>
            <v-flex xs-6>
              <v-card>
                <v-card-title primary-title>
                    <v-flex align-center>
                    <h2>Edit or Delete Reason</h2>
                    </v-flex>
                </v-card-title>

                  <v-container fill-height fluid pa-2 >
                    <v-layout fill-height>
                      <v-flex xs12 sm4 >
                        <v-select
                          :items="damageReasons.departments"
                          v-model="department"
                          label="Choose Department"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm4 v-if="department == 'order'">
                        <v-select
                          :items="damageReasons.order.reasons"
                          v-model="reason"
                          label="Damage Reason to Edit"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm4 v-if="department == 'warehouse'">
                        <v-select
                          :items="damageReasons.warehouse.reasons"
                          v-model="reason"
                          label="Damage Reason to Edit"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm4 v-if="reason">
                        <v-text-field
                          required v-model="updatedReason" label="Update Reason">
                        </v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>

                <v-card-actions>
                  <v-layout row wrap justify-center>
                    <v-flex xs2 >
                      <v-btn color="success" v-if="updatedReason"
                        @click="updateReason"
                        >
                        Update
                      </v-btn>
                    </v-flex>
                    <v-flex xs2 >
                      <v-btn color="error" v-if="reason"
                        @click="deleteReason"
                        >
                        Delete
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-actions>
              </v-card>
            </v-flex>

            <!-- Second card -->
            <v-flex xs-6>
              <v-card>
                <v-card-title primary-title>
                    <v-flex align-center>
                    <h2>Add New Reason</h2>
                    </v-flex>
                </v-card-title>

                  <v-container fill-height fluid pa-2 >
                    <v-layout fill-height>
                      <v-flex xs12 sm4 >
                        <v-select
                          :items="damageReasons.departments"
                          v-model="newDepartment"
                          label="Choose Department"
                          single-line
                          required
                        ></v-select>
                      </v-flex>
                      <v-flex xs12 sm4 v-if="newDepartment">
                        <v-text-field
                          required v-model="newReason" label="Add New Reason">
                        </v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>

                <v-card-actions>
                  <v-layout row wrap justify-center>
                    <v-flex xs2 >
                      <v-btn color="info" v-if="newReason"
                        @click="addReason"
                        >
                        Add
                      </v-btn>
                    </v-flex>
                  </v-layout>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
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
      newReason: '',
      newDepartment: ''
    }
  },
  methods: {
    clearfields() {
      this.department = ''
      this.reason = ''
      this.updatedReason = ''
      this.newReason = ''
      this.newDepartment = ''
    },
    updateReason() {
      let reasons = this.damageReasons[this.department].reasons
      let index = reasons.indexOf(this.reason)
      reasons[index] = this.updatedReason
      this.damageReasons[this.department].reasons = reasons

      this.updateDatabase(reasons, this.department)
      this.clearfields()
    },
    addReason() {
      let reasons = this.damageReasons[this.newDepartment].reasons
      this.damageReasons[this.newDepartment].reasons.push(this.newReason)

      this.updateDatabase(reasons, this.newDepartment)
      this.clearfields()
    },

    updateDatabase(reasons, department) {
      // update database
      db
        .collection('damageReasons')
        .doc(department)
        .set(
          {
            reasons
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => console.log)
    },
    deleteReason() {
      let reasons = this.damageReasons.order.reasons
      let index = reasons.indexOf(this.reason)
      confirm('Are you sure you want to delete this item?') &&
        (reasons.splice(index, 1),
        (this.damageReasons.order.reasons = reasons),
        this.updateDatabase(reasons, this.department))
      this.clearfields()
    }
  }
}
</script>

<style>
</style>
