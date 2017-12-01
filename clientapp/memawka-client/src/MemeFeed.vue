<template>
  <div class="container">
    <image-box v-for="(meme, index) in memes" :key="index" :meme="meme"></image-box>
  </div>
</template>

<script>
  import axios from 'axios'
  import ImageBox from './components/ImageBox.vue'
  export default {
    name: 'MemeFeed',
    components: { ImageBox },
    data: () => {
      return {
        memes: []
      }
    },
    created: function () {
      axios.get('http://165.227.133.227:8090/memes/memes/')
        .then(response => {
          this.memes = response.data.results
        })
      console.log(this.memes)
    }
  }
</script>

<style scoped>

</style>
