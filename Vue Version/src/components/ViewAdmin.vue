<template>
  <v-container class="view-admin" text-xs-center fill-height>
    <v-layout row wrap align-center justify-center>
      <v-flex xs12 sm10>
        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Admin Options</h2>
            </v-flex>
          </v-card-title>
          <v-card-text>
            <v-layout row wrap>
              <v-flex xs12 sm6>
              <v-btn color="purple darken-1 white--text" @click="editReasons = !editReasons">Edit Damage Reasons</v-btn>
            </v-flex>
            <v-flex xs12 sm6>
              <v-btn color="purple darken-1 white--text" @click="editCosts = !editCosts">Edit Product Costs</v-btn>
            </v-flex>
            </v-layout>
          </v-card-text>
          <v-card-text>
            <edit-damage-reasons v-if="editReasons" :damageReasons="damageReasons"></edit-damage-reasons>
            <edit-product-costs v-if="editCosts" :productCosts="productCosts"></edit-product-costs>
          </v-card-text>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import EditDamageReasons from '@/components/EditDamageReasons'
import EditProductCosts from '@/components/EditProductCosts'
import db from '@/firebase/init'
export default {
  name: 'ViewAdmin',
  components: {
    EditProductCosts,
    EditDamageReasons
  },
  data() {
    return {
      editReasons: false,
      editCosts: false,
      damageReasons: [],
      productCosts: []
    }
  },
  created() {
    // fetch data from firestore
    db
      .collection('productCosts')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.productCosts.push(doc.data())
        })
      })
      .catch(err => console.log(err))

    db
      .collection('damageReasons')
      .get()
      .then(snapshot => {
        snapshot.forEach(doc => {
          this.damageReasons.push(doc.data())
        })
      })
      .catch(err => console.log(err))
  }
}
</script>
