import Vue from 'vue'
import Vuex from 'vuex'
import axiosInstance from '../http-common'
Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    loggedUser: null
  },
  getters: {
    loggedUser: state => {
      return state.loggedUser
    }
  },
  mutations: {
    logUserIn: (state, payload) => {
      state.loggedUser = payload
    }
  },
  actions: {
    refreshUser: ({commit}) => {
      axiosInstance.get('/memes/get-owner/')
        .then((response) => {
          commit('logUserIn', response.data.author)
        })
        .catch((err) => {
          console.log(err)
          commit('logUserIn', null)
        })
    }
  }
})
