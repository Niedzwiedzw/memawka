<template>
  <div class="card app-main-card">
    <img class="card-img-top" :src="meme.image_url" alt="Card image cap">
    <div class="card-body">
      <h4 class="card-title">{{ meme.reaction_count }} <i style="color: red;" class="fa fa-star"></i></h4>
      <p class="card-text" :title="humanDate">
        <strong><router-link :to="'/profile/' + meme.author.id">[{{ timeSinceAdded }}] {{meme.author.name}} </router-link></strong>{{ meme.message }}</p>
      <a target="_blank" :href="facebook_link" class="btn btn-primary">Zobacz ten mem na grupie</a>
    </div>
  </div>
</template>

<script>
  import moment from 'moment'
  export default {
    name: 'image-box',
    props: ['meme'],
    mounted () {
      let memeid = this.meme.facebook_id.split('_')
      this.facebook_link = 'https://www.facebook.com/groups/' + memeid[0] + '/permalink/' + memeid[1]
      this.timeSinceAdded = moment(this.meme.creation).fromNow()
      this.humanDate = moment(this.meme.creation).format('DD.MM.YYYY h:mm:ss a')
    },
    data () {
      return {
        facebook_link: 'www.google.com'
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
