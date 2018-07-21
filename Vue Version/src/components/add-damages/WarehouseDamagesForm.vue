<template>
  <v-layout row wrap justify-center  class="warehouse-damages-form">
    <v-flex xs8 sm4 mx-4>
      <v-select
        :items="damageReasons.warehouse.reasons"
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
    <v-flex xs6 sm3 mx-4>
      <v-text-field
        name="itemsLost"
        label="# Lost"
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
  name: 'WarehouseDamagesForm',
  props: ['damageReasons', 'damageReport', 'productCosts'],
  data() {
    return {}
  }
}
</script>

<style>
</style>
