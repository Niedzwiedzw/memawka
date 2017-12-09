<template>
  <div class="row">
    <div class="col-4">
      <router-link :to="'/profile/' + comment.author.id">
        <img
          :src="comment.author.display_avatar"
          :alt="'Awatar uzytkownika ' + comment.author.display_name"
          class="img-responsive img-thumbnail"/>
      </router-link>
    </div>
    <section :id="'comment-' + comment.id">
      <div class="col-8">
        <div class="row">
          <h3 class="pull-left">
            <router-link :to="'/profile/' + comment.author.id">
              ~ {{ comment.author.display_name }}
            </router-link>
            <router-link :to="'/meme/' + meme.id + '#comment-' + comment.id">
              <small>{{ humanDate }}</small>
            </router-link>
          </h3>
        </div>
        <div class="row">
          <p>{{ comment.message }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  import moment from 'moment'
  export default {
    name: 'AppComment',
    props: ['comment', 'meme'],
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

</style>
