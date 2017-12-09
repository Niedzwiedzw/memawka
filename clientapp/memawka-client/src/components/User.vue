<template>
  <div class="container">
    <div class="card container">
      <img class="card-img-top" :src="user.display_avatar" alt="Card image cap">
      <div class="card-body">
        <button
          v-if="myProfile"
          @click="toggleRealPhoto"
          class="btn-btn-lg btn-info"><i class="fa fa-unlock"></i> Odkryj swoje zdjecie</button>
        <hr>
        <h4 class="card-title">{{user.display_name}}</h4>
        <button
          v-if="myProfile"
          @click="toggleRealName"
          class="btn-btn-lg btn-info"><i class="fa fa-unlock"></i> Odkryj swoją nazwę użytkownika</button>

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
        <div v-if="user.memes[0]['facebook_id']" class="col-lg-4 col-md-6 col-sm-6"  v-for="meme in user.memes">
          <image-box :meme="meme"></image-box>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axiosInstance from '../http-common'
  import { mapGetters, mapActions } from 'vuex'
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
        if (this.loggedUser === null) {
          return false
        } else {
          return this.loggedUser.id === parseInt(this.$route.params['id'])
        }
      }
    },
    methods: {
      ...mapActions([
        'refreshUser'
      ]),
      getProfile (id) {
        axiosInstance.get('/memes/authors/' + id + '/')
          .then((response) => {
            this.user = response.data
          })
      },
      toggleRealPhoto () {
        axiosInstance.get('/memes/toggle-real-photo/')
          .then((response) => {
            console.log(response.data)
            this.getProfile(this.loggedUser.id)
          })
      },
      toggleRealName () {
        axiosInstance.get('/memes/toggle-real-name/')
          .then((response) => {
            console.log(response.data)
            this.getProfile(this.loggedUser.id)
          })
      }
    },
    created () {
      this.refreshUser()
      this.getProfile(this.$route.params['id'])
    }
  }
</script>

<style scoped>
  .row {
    margin-top: 2em;
  }
</style>
