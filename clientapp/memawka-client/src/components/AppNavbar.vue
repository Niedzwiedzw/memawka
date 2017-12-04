<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand" to="/">Memawka</router-link>
    <router-link class="navbar-brand" to="/profile/123">User</router-link>

  </nav>
</template>

<script>
  export default {
    name: 'app-navbar',
    data () {
      return {
      }
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
