// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import moment from 'moment'
import 'bootstrap/dist/css/bootstrap.css'
import VueCookie from 'vue-cookie'

Vue.config.productionTip = false

/* eslint-disable no-new */
let mainVue = new Vue({
  el: '#app',
  router,
  moment,
  template: '<App/>',
  components: { App }
})

mainVue.use(VueCookie)
