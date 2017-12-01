<template>
  <div class="card app-main-card">
    <img class="card-img-top" :src="meme.image_url" alt="Card image cap">
    <div class="card-body">
      <h4 class="card-title">{{ meme.reaction_count }} <i style="color: red;" class="fa fa-star"></i></h4>
      <p class="card-text">{{ meme.message }}</p>
      <a href="https://www.facebook.com/groups/jbwamem/permalink/1677854812258843/" class="btn btn-primary">Zobacz ten mem na grupie</a>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'image-box',
    props: ['meme'],
    data () {
      return {
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
