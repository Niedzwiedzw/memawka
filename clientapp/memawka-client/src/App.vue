<template>
  <div id="app">
    <app-navbar></app-navbar>
    <div class="container">
      <image-box v-for="index in 3"></image-box>
    </div>
  </div>
</template>

<script>
  import AppNavbar from './components/AppNavbar.vue'
  import ImageBox from './components/ImageBox.vue'
  export default {
    name: 'app',
    components: { AppNavbar, ImageBox }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  .blue {
    background-color: lightblue;
    border: 1px solid blue;
  }
</style>
