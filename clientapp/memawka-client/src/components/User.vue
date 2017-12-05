<template>
  <div class="container">
    <div class="card container">
      <img class="card-img-top" :src="user.display_avatar" alt="Card image cap">
      <div class="card-body">
        <button class="btn-btn-lg btn-info"><i class="fa fa-unlock"></i> Odkryj swoje zdjecie</button>
        <hr>
        <h4 class="card-title">{{user.display_name}}</h4>
        <button class="btn-btn-lg btn-info"><i class="fa fa-unlock"></i> Odkryj swoją nazwę użytkownika</button>

        <p class="card-text">Suma lajkow: <strong>{{ user.reaction_sum.reaction_count__sum }}</strong></p>
      </div>
      <ul class="list-group list-group-flush">

        <li class="list-group-item">
          <h2>
            GRUPY
            <br>
            <span class="badge badge-success">Memawka</span>
            <span v-for="i in 4" class="badge badge-secondary">Gownawka</span>
          </h2>
        </li>
      </ul>
      <div class="row">
        <div class="col-lg-4 col-md-6 col-sm-6"  v-for="meme in user.memes">
          <div class="card-body">
            <div class="card" style="width: 20rem;">
              <img class="card-img-top" :src="meme.image_url" alt="Card image cap">
              <div class="card-body">
                <h4 class="card-title">{{meme.reaction_count}} likes</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axiosInstance from '../http-common'
  import { mapGetters } from 'vuex'
  export default {
    name: 'User',
    data () {
      return {
        user: {
          memes: [
            {
              reaction_count: 0,
              image_url: ''
            }],
          reaction_sum: 0
        }
      }
    },
    computed: {
      ...mapGetters([
        'loggedUser'
      ]),
      myProfile () {
        return this.loggedUser.id === this.$route.params['id']
      }
    },
    methods: {
      getProfile (id) {
        axiosInstance.get('/memes/authors/' + id + '/')
          .then((response) => {
            this.user = response.data
          })
      }},
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
