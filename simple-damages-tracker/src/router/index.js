import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import AddDamages from '@/components/AddDamages'
import ViewDamages from '@/components/ViewDamages'
import ViewOrderDamages from '@/components/ViewOrderDamages'
import ViewWarehouseDamages from '@/components/ViewWarehouseDamages'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/add-damages',
      name: 'AddDamages',
      component: AddDamages
    },
    {
      path: '/view-damages',
      name: 'ViewDamages',
      component: ViewDamages
    },
    {
      path: '/order-damages',
      name: 'ViewOrderDamages',
      component: ViewOrderDamages
    },
    {
      path: '/warehouse-damages',
      name: 'ViewWarehouseDamages',
      component: ViewWarehouseDamages
    }
  ]
})
