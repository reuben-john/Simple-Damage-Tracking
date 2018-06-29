import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import AddDamages from '@/components/add-damages/AddDamages'
import ViewOrderDamages from '@/components/view-damages/ViewOrderDamages'
import ViewWarehouseDamages from '@/components/view-damages/ViewWarehouseDamages'
import ViewAdmin from '@/components/admin/ViewAdmin'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
      path: '/order-damages',
      name: 'ViewOrderDamages',
      component: ViewOrderDamages
    },
    {
      path: '/warehouse-damages',
      name: 'ViewWarehouseDamages',
      component: ViewWarehouseDamages
    },
    {
      path: '/admin',
      name: 'ViewAdmin',
      component: ViewAdmin
    }
  ]
})
