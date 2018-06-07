<template>
<div class="view-warehouse-damages">
  <h2>View Warehouse Damages</h2>
</div>
</template>

<script>
export default {
  name: 'ViewWarehouseDamages',
  data() {
    return {
      warehouseDamages: [
        {
          date: '01/05/2018',
          numberLost: '1',
          cost: '20.00',
          itemType: 'food',
          lossType: 'Item Loss'
        },
        {
          date: '02/05/2018',
          numberLost: '5',
          itemCost: '30.00',
          itemType: 'general',
          lossType: 'Item Loss'
        },
        {
          date: '02/05/2018',
          numberLost: '1',
          cost: '40.00',
          itemType: 'beauty',
          lossType: 'Box Loss'
        }
      ]
    }
  }
}
</script>

<style>
</style>

