import Vue from 'vue'
import Router from 'vue-router'
import MemeFeed from '../MemeFeed.vue'
import User from '../components/User.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/profile/:id',
      name: 'User',
      component: User
    },
    {
      path: '/',
      name: 'MemeFeed',
      component: MemeFeed
    }

  ]
})
