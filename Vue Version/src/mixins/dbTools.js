import db from '@/firebase/init'
import moment from 'moment'

export default {
  name: 'dbTools',
  methods: {
    hello () {
      console.log('hello from mixin!')
    },
    tallyNewOrderTotals () {
      // Tallies total damages for orders

      let damagesRef = db.collection('damages')
      let orderTally = 0
      let shippingTally = 0

      // Tally order totals
      let orderQuery = damagesRef
        .where('damageDept', '==', 'order')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let cost = doc.data().itemCost
            let numLost = doc.data().itemsLost
            let shipCost = doc.data().shippingCost
            let shipLost = doc.data().shippingLost
            let returnCost = 0
            let currentYear = moment().format('YYYY')
            let year = moment(doc.data().timestamp).format('YYYY')
            if (doc.data().returnCost) {
              returnCost = doc.data().returnCost
            }
            if (currentYear === year) {
              shippingTally += shipLost + returnCost
              orderTally += cost * numLost
            }
          })
          // Normalize cost to 2 decimal places so it is accurate for money display $xx.xx
          orderTally = parseFloat(orderTally.toFixed(2))
          shippingTally = parseFloat(shippingTally.toFixed(2))
          this.updateOrderTally(orderTally, shippingTally)
        })
        .catch(err => {
          console.log(err)
        })
    },
    tallyNewWarehouseTotals () {
      // Tallies total damages for warehouse
      let damagesRef = db.collection('damages')
      let warehouseTally = 0
      // Tally warehouse totals
      let warehouseQuery = damagesRef
        .where('damageDept', '==', 'warehouse')
        .get()
        .then(snapshot => {
          snapshot.forEach(doc => {
            let cost = doc.data().itemCost
            let numLost = doc.data().itemsLost
            let currentYear = moment().format('YYYY')
            let year = moment(doc.data().timestamp).format('YYYY')
            if (currentYear === year) {
              warehouseTally += cost * numLost
            }
          })
          // Normalize cost to 2 decimal places so it is accurate for money display $xx.xx
          warehouseTally = parseFloat(warehouseTally.toFixed(2))
          this.updateWarehouseTally(warehouseTally)
          // console.log(warehouseTally)
        })
        .catch(err => {
          console.log(err)
        })
    },
    updateWarehouseTally (tally) {
      // Update warehouse tally in firestore
      db.collection('totalLosses')
        .doc('warehouse')
        .set(
          {
            total: tally
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    },
    updateOrderTally (orderTally, shippingTally) {
      // Update order tally in firestore

      // Update tally in firestore
      db.collection('totalLosses')
        .doc('order')
        .set(
          {
            total: parseFloat((orderTally + shippingTally).toFixed(2)),
            itemTotal: orderTally,
            shipTotal: shippingTally
          },
          { merge: true }
        )
        .then(console.log('Updated'))
        .catch(err => {
          console.log(err)
        })
    },
    deleteFromDB (itemId) {
      // Deletes damage report from firestore

      let damagesRef = db.collection('damages').doc(itemId)
      // fetch data from firestore
      let query = damagesRef
        .delete()
        .then(console.log('Deleted'))
        .catch(err => {
          console.log(err)
        })
    }
  }
}
