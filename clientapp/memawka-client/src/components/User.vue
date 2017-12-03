<template>
  <div class="container">
    <div class="card container">
      <img class="card-img-top" :src="user.memes[0].image_url" alt="Card image cap">
      <div class="card-body">
        <h4 class="card-title">{{user.name}}</h4>
        <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>

        <p class="card-text">Suma lajkow: <strong>{{ user.reaction_sum.reaction_count__sum }}</strong></p>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <h2>
            GRUPY
            <br>
            <span class="badge badge-success">Memawka</span>
            <span v-for="i in 12" class="badge badge-secondary">Gownawka</span>
          </h2>
        </li>
        <li class="list-group-item">Dapibus ac facilisis in</li>
        <li class="list-group-item">Vestibulum at eros</li>
      </ul>
      <div class="card-body">
        <a href="#" class="card-link">Card link</a>
        <a href="#" class="card-link">Another link</a>
      </div>
      <div class="row">
        <div class="col-lg-4 col-md-6 col-sm-6"  v-for="meme in user.memes">
          <div class="card-body">
            <div class="card" style="width: 20rem;">
              <img class="card-img-top" :src="meme.image_url" alt="Card image cap">
              <div class="card-body">
                <h4 class="card-title">{{meme.reaction_count}} likes</h4>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                <a href="#" class="btn btn-primary">Go somewhere</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'User',
    data () {
      return {
        user: null
      }
    },
    methods: {
      getProfile (id) {
        axios.get('http://127.0.0.1:8000/memes/authors/' + id)
          .then((response) => {
            this.user = response.data
            console.log(this.user)
          })
      }
    },
    created () {
      this.getProfile(this.$route.params['id'])
    }
  }
</script>

<style scoped>
  #app-avatar {
    border-radius: 50%;
    object-fit: cover;
  }
  .row {
    margin-top: 2em;
  }
</style>
