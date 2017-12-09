// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { store } from './store'
import moment from 'moment'
import vueScrollto from 'vue-scrollto'
import ImageBox from './components/ImageBox.vue'
import AppComment from './components/AppComment.vue'
import 'bootstrap/dist/css/bootstrap.css'

Vue.config.productionTip = false

Vue.component('image-box', ImageBox)
Vue.component('app-comment', AppComment)

Vue.use(vueScrollto)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  moment,
  store,
  template: '<App/>',
  components: { App }
})
