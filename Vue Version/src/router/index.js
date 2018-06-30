import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/home/Index'
import AddDamages from '@/components/add-damages/AddDamages'
import ViewOrderDamages from '@/components/view-damages/ViewOrderDamages'
import ViewWarehouseDamages from '@/components/view-damages/ViewWarehouseDamages'
import ViewAdmin from '@/components/admin/ViewAdmin'
import Login from '@/components/auth/Login'
import firebase from 'firebase'

Vue.use(Router)

const router = new Router({
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
      component: ViewOrderDamages,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/warehouse-damages',
      name: 'ViewWarehouseDamages',
      component: ViewWarehouseDamages,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/admin',
      name: 'ViewAdmin',
      component: ViewAdmin,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})

router.beforeEach((to, from, next) => {
  // Check if route requires auth
  if (to.matched.some(rec => rec.meta.requiresAuth)) {
    // check auth state of user
    let user = firebase.auth().currentUser
    if (user) {
      // user signed in, proceed to route
      next()
    } else {
      // no user signed in
      next({ name: 'Login' })
    }
  } else {
    next()
  }
})

export default router
