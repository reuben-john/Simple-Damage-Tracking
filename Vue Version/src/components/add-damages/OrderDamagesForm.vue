<template>
  <v-layout row wrap justify-center  class="order-damages-form">
    <v-flex xs8 sm4 mx-4>
      <v-select
        :items="damageReasons.order.reasons"
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
        type="number"
        required
      ></v-text-field>
    </v-flex>
    <v-flex xs6 sm3 mx-3>
      <v-text-field
        name="orderTotal"
        label="Order Total"
        id="order-total"
        v-model="damageReport.orderTotal"
        type="number"
        required
      ></v-text-field>
    </v-flex>
    <v-flex xs6 sm3 mx-3>
      <v-text-field
        name="shippingCost"
        label="Shipping Cost"
        id="shipping-cost"
        v-model="damageReport.shippingCost"
        type="number"
        required
      ></v-text-field>
    </v-flex>
    <v-flex xs6 sm3 mx-4>
      <v-text-field
        name="shippingLost"
        label="Shipping Lost"
        id="shipping-lost"
        v-model="damageReport.shippingLost"
        type="number"
        required
      ></v-text-field>
    </v-flex>
    <v-flex xs6 sm3 mx-4>
      <v-text-field
        name="itemsLost"
        label="Items Lost"
        id="items-lost"
        v-model="damageReport.itemsLost"
        type="number"
        required
      ></v-text-field>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'OrderDamagesForm',
  props: ['damageReasons', 'damageReport', 'productCosts'],
  data() {
    return {}
  }
}
</script>

<style>
</style>
