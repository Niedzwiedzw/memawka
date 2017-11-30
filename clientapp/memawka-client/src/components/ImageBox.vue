<template>
  <div class="card app-main-card">
    <img class="card-img-top" :src="imageUrl" alt="Card image cap">
    <div class="card-body">
      <h4 class="card-title">Card title</h4>
      <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
      <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'image-box',
    data () {
      return {
        imageUrl: 'https://scontent.xx.fbcdn.net/v/t1.0-9/s720x720/22851900_153911322011714_4302665789563309979_n.jpg?oh=13aeb63eb9e1ae7cf48a3baeaa8731fd&oe=5A94D091'
      }
    }
  }
</script>

<style scoped>
  .app-main-card {
    margin-left: auto;
    margin-top: 3em;
    margin-bottom: 3em;
  }
</style>
