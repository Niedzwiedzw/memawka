<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand" to="/">Memawka</router-link>
    <router-link v-if="loggedUser" class="navbar-brand" :to="'/profile/'+loggedUser.id+'/'">Moje konto</router-link>
    <a class="navbar-brand" href="http://127.0.0.1:8000/accounts/facebook/login">
      {{loggedUser ? 'Witaj ' + loggedUser.name : 'Zaloguj sie z uzyciem Facebooka' }}
    </a>
  </nav>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex'
  export default {
    name: 'app-navbar',
    data () {
      return {
      }
    },
    methods: {
      ...mapActions([
        'refreshUser'
      ])
    },
    computed: {
      ...mapGetters([
        'loggedUser'
      ])
    },
    created () {
      setInterval(this.refreshUser, 5000)
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
  .router-link-exact-active {
    background-color: red;
  }
</style>
