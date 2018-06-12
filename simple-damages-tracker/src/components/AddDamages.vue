// TODO Move order form to seperate vue template and load it in when needed.
// TODO Create warehouse form
// TODO Add form validation to validate numbers
// TODO Ensure all data that should be numbers gets converted before adding it to the d-block
// TODO Update the total damages tallies before returning to the Index page


<template>
  <div class="add-damages">
    <v-container text-xs-center>
      <v-layout row wrap align-center>
        <v-flex xs12 sm6 offset-sm1 offset-md2>
          <v-card>
            <v-card-title primary-title>
              <v-flex>
                <h1>Add Damage Report</h1>
              </v-flex>
            </v-card-title>
            <v-form>

              <v-card-text v-if="damageReasons">
                <h4>What type of damage do you wish to log?</h4>
                <v-radio-group
                v-model="damageReport.damageDept">
                  <v-layout row wrap>
                      <v-flex xs12 sm6
                      v-for="(reason, index) in damageReasons.reasons"
                      :key="index">
                        <v-radio
                          :key="reason"
                          :label="`${reason} damage report`"
                          :value="reason"
                        ></v-radio>
                      </v-flex>
                        <h2>{{damageDept}}</h2>
                      </v-layout>
                    </v-radio-group>
                  <v-layout v-if="damageReport.damageDept == 'order'">
                    <OrderDamagesForm :damageReasons="damageReasons" :damageReport="damageReport" :productCosts="productCosts"></OrderDamagesForm>
                  <!-- <v-flex xs8 sm4 mx-4>
                    <v-select
                      :items="damageReasons.order.type"
                      v-model="damageReport.reasonLost"
                      label="Damage Type"
                      single-line
                      required
                    ></v-select>
                  </v-flex>
                  <v-flex xs8 sm4 mx-4>
                    <v-select
                      :items="productCosts.types"
                      v-model="damageReport.itemType"
                      label="Product Type"
                      single-line
                      required
                    ></v-select>
                  </v-flex>
                  <v-flex xs6 sm3 mx-3>
                    <v-text-field
                      name="orderNumber"
                      label="Order Number"
                      id="order-number"
                      v-model="damageReport.orderNumber"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs6 sm3 mx-3>
                    <v-text-field
                      name="orderTotal"
                      label="Order Total"
                      id="order-total"
                      v-model="damageReport.orderTotal"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs6 sm3 mx-3>
                    <v-text-field
                      name="shippingCost"
                      label="Shipping Cost"
                      id="shipping-cost"
                      v-model="damageReport.shippingCost"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs6 sm3 mx-4>
                    <v-text-field
                      name="shippingLost"
                      label="Shipping Lost"
                      id="shipping-lost"
                      v-model="damageReport.shippingLost"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs6 sm3 mx-4>
                    <v-text-field
                      name="itemsLost"
                      label="Items Lost"
                      id="items-lost"
                      v-model="damageReport.itemsLost"
                    ></v-text-field>
                  </v-flex> -->
                </v-layout>
              </v-card-text>
              <v-btn
                @click="submit"
              >
              Submit
            </v-btn>
            </v-form>
          </v-card>
        <p><b>Current Damage Report</b>: {{ damageReport }}</p>
        </v-flex>
      </v-layout>
      {{ productCosts }}
    </v-container>
  </div>
</template>

<script>
import db from '@/firebase/init'
import OrderDamagesForm from '@/components/OrderDamagesForm'

export default {
  name: 'AddDamages',
  components: {
    OrderDamagesForm
  },
  data() {
    return {
      appData: {},
      productCosts: null,
      damageReasons: null,
      damageDept: null,
      damageReport: {}
    }
  },
  methods: {
    addDamages() {
      return {}
    },
    submit() {
      console.log(this.damageReport)
      // Add timestamp to report
      this.damageReport.timestamp = Date.now()

      // Pull product cost for a box loss if damage report is for bad box
      // Otherwise default to individual item cost
      if (this.damageReport.reasonLost == 'Bad Box') {
        this.damageReport.itemCost = this.productCosts[this.damageReport.itemType].boxCost
      } else {
        this.damageReport.itemCost = this.productCosts[this.damageReport.itemType].itemCost
      }

      // Assign report to variable before submitting
      // TODO look into this - Was having an issue on the data not going to the database without this
      let report = this.damageReport
      // Send damage report to database
      db
        .collection('damages')
        .add(report)
        .then(() => {
          this.$router.push({ name: 'Index' })
        })
        .catch(err => console.log(err))
    }
  },
  created() {
    // Get damage reasons from firestore
    db
      .collection('appData')
      .doc('damageReasons')
      .get()
      .then(doc => {
        this.damageReasons = doc.data()
        this.damageReasons.reasons = Object.keys(this.damageReasons)
      })
      .catch(err => {
        console.log(err)
      })

    // Get product costs from firestore
    db
      .collection('appData')
      .doc('productCosts')
      .get()
      .then(doc => {
        this.productCosts = doc.data()
        this.productCosts.types = Object.keys(this.productCosts)
      })
      .catch(err => {
        console.log(err)
      })
  }
}
</script>

<style>
</style>
