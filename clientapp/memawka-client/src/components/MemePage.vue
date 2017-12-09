<template>
  <div class="container">
    <div class="container">
      <image-box v-if="meme !== null" :meme="meme"></image-box>
      <div class="container" v-if="meme && meme.comments.length > -1">
        <app-comment
          v-for="comment in meme.comments"
          :comment="comment"
          :meme="meme"></app-comment>
      </div>
    </div>


    <div class="form-group comment-form" v-if="this.loggedUser !== null">
      <div class="row">
        <div class="col-4">
          <button
            @click="commentMeme(meme.id)"
            class="btn app-btn-full btn-info">skomentuj</button>
        </div>
        <div class="col-8">
          <label for="comment"></label>
          <textarea
            v-model="message"
            class="form-control" rows="5" id="comment"></textarea>
        </div>
      </div>
    </div>

    <div v-else><p class="text-info">Musisz być zalogowany aby komentować</p></div>
  </div>
</template>

<script>
  import axiosInstance from '../http-common'
  import { mapGetters } from 'vuex'
  import AppComment from './AppComment.vue'
  export default {
    components: {AppComment},
    name: 'MemePage',
    data () {
      return {
        meme: null,
        message: ''
      }
    },
    methods: {
      getMeme (id) {
        axiosInstance.get('/memes/memes/' + id + '/')
          .then((response) => {
            this.$set(this, 'meme', response.data)
          })
      },
      commentMeme (memeId) {
        console.log(memeId)
        if (this.message !== '') {
          axiosInstance.post(
            '/memes/memes/' + memeId + '/comments/',
            {
              'message': this.message,
              'commented_object': memeId,
              'author': this.loggedUser ? this.loggedUser.id : 0})
            .then((response) => {
              this.getMeme(memeId)
              this.message = ''
            })
        }
      }
    },
    computed: {
      ...mapGetters([
        'loggedUser'
      ])
    },
    created () {
      this.getMeme(this.$route.params['id'])
    }
  }
</script>

<style scoped>
  .app-user-avatar {
    width: 8em;
  }
  .app-btn-full {
    margin-top: 1em;
    width: 100%;
    height: 100%
  }

  .comment-form {
    margin-top: 2em;
    margin-bottom: 4em;
  }

</style>
