<template>
  <div id="app">
    <app-navbar></app-navbar>
    <div class="container">
      <meme-feed></meme-feed>
    </div>
  </div>
</template>

<script>
  import AppNavbar from './components/AppNavbar.vue'
  import ImageBox from './components/ImageBox.vue'
  import MemeFeed from './MemeFeed.vue'
  export default {
    name: 'app',
    components: { AppNavbar, ImageBox, MemeFeed }
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
