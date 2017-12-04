<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand" to="/">Memawka</router-link>
    <router-link v-if="loggedUser" class="navbar-brand" :to="'/profile/'+loggedUser.id+'/'">Konto</router-link>
    <a class="navbar-brand" href="http://127.0.0.1:8000/accounts/facebook/login">
      {{loggedUser ? 'Witaj ' + loggedUser.name : 'Zaloguj sie z uzyciem Facebooka' }}
    </a>
  </nav>
</template>

<script>
  import axiosInstance from '../http-common'
  export default {
    name: 'app-navbar',
    data () {
      return {
        loggedUser: null
      }
    },
    methods: {
      getLoggedUser () {
        axiosInstance.get('/memes/get-owner/')
          .then((response) => {
            this.loggedUser = response.data.author
            setTimeout(this.getLoggedUser, 5000)
          })
      }
    },
    created () {
      this.getLoggedUser()
    }
  }
</script>

<style scoped>
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 3;
  }
</style>
