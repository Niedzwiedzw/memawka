<template>
  <div class="row">
    <div class="col-3">
      <img
        :src="comment.author.display_avatar"
        :alt="'Zdjecie' + comment.author.display_name"
        class="image-responsive hoverable img-thumbnail app-avatar"
        @click="getUserProfile"
      >
    </div>
    <div class="col-9">
      <div class="row">
        <div @click="getUserProfile" class="container hoverable app-comment-author font-weight-bold">{{ comment.author.display_name }}</div>
      </div>
      <div class="row">
        <div class="container hoverable app-comment-date font-italic">{{ humanDate }}</div>
      </div>
      <div class="row">
        <div class="container app-comment-message">
          {{ comment.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import moment from 'moment'
  export default {
    name: 'AppComment',
    props: ['comment', 'meme'],
    methods: {
      getUserProfile() {
        this.$router.push('/profile/' + this.comment.author.id + '/')
      }
    },
    data () {
      return {}
    },
    computed: {
      humanDate () {
        return this.comment.created ? moment(this.comment.created).fromNow() : ''
      }
    }
  }
</script>

<style scoped>
  .app-comment-author, .app-comment-date, .app-comment-message {
    text-align: left;
  }

  .app-comment-message {
    word-wrap: break-word;
  }

  .app-avatar {
    cursor: alias;
  }
</style>
