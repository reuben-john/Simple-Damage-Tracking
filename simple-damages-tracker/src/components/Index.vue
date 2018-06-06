<template>
  <div class="index container">
    <div class="collection" v-for="loss in orderDamages" :key="loss.orderNumber">
        <a class="collection-item">Order Number: {{ loss.orderNumber }}</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      orderDamages: [
        {
          date: '01/05/2018',
          orderNumber: '5',
          orderCost: '5.99',
          shippingCost: '2.61',
          shippingLoss: '2.61',
          itemType: 'beauty',
          itemCost: '1',
          itemsLost: '2',
          lossType: 'Bad Product'
        },
        {
          date: '02/05/2018',
          orderNumber: '25',
          orderCost: '15.99',
          shippingCost: '5.61',
          shippingLoss: '3.61',
          itemType: 'clothing',
          itemCost: '4',
          itemsLost: '0',
          lossType: 'Returned Product'
        },
        {
          date: '02/05/2018',
          orderNumber: '15',
          orderCost: '8.99',
          shippingCost: '2.61',
          shippingLoss: '2.61',
          itemType: 'makeup',
          itemCost: '0.3',
          itemsLost: '1',
          lossType: 'Returned Product'
        }
      ]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.index {
  margin: 20px auto;
}
.collection {
  margin: 0 auto;
}
</style>
