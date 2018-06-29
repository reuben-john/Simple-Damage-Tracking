<template>
        <v-card>
          <v-card-title primary-title>
            <v-flex>
              <h2>Product Costs</h2>
              <li v-for="(cost, index) in productCosts" :key="index"> {{cost.name}}</li>
            </v-flex>
          </v-card-title>
          <v-card-text>

          </v-card-text>
        </v-card>

</template>

<script>
export default {
  name: 'EditProductCosts',
  props: ['productCosts'],
  data() {
    return {}
  }
}
</script>

<style>
</style>
