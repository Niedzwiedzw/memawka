<template>
  <div class="container">
    <!--pagination-->
    <div class="container">
      <ul class="pagination pagination-lg justify-content-center">
        <li class="page-item" @click="getPage(page - 1)" :class="{disabled: page == 1}"><a class="page-link">Previous</a></li>

        <template v-if="page>5">
          <li class="page-item" @click="getPage(1)"><a class="page-link">1</a></li>
          <li class="page-item disabled"><a class="page-link">...</a></li>
        </template>

        <li class="page-item"
            v-for="index in 10"
            v-if="page + index - 5 <= numberOfPages && page + index - 5 > 0"
            @click="getPage(page + index - 5)"
            :class="{active:  index - 5 == 0}">
          <a class="page-link">
            {{ page + index - 5 }}
          </a>
        </li>


        <template v-if="page < numberOfPages - 5">
          <li class="page-item disabled"><a class="page-link">...</a></li>
          <li class="page-item" @click="getPage(numberOfPages)"><a class="page-link">{{numberOfPages}}</a></li>
        </template>

        <li class="page-item" @click="getPage(page+1)" :class="{disabled: page == numberOfPages}"><a class="page-link">Next</a></li>
      </ul>
    </div>

    <!--content-->
    <div class="container">
      <div class="row">
        <div class="col-12" v-for="(meme, index) in memes" :key="index">
          <image-box :meme="meme"></image-box>
        </div>
      </div>
    </div>
    <!--bottom pagination-->
    <div class="container">
      <ul class="pagination pagination-lg justify-content-center">
        <li class="page-item" @click="getPage(page - 1)" :class="{disabled: page == 1}"><a class="page-link">Previous</a></li>

        <template v-if="page>5">
          <li class="page-item" @click="getPage(1)"><a class="page-link">1</a></li>
          <li class="page-item disabled"><a class="page-link">...</a></li>
        </template>

        <li class="page-item"
            v-for="index in 10"
            v-if="page + index - 5 <= numberOfPages && page + index - 5 > 0"
            @click="getPage(page + index - 5)"
            :class="{active:  index - 5 == 0}">
          <a class="page-link">
            {{ page + index - 5 }}
          </a>
        </li>


        <template v-if="page < numberOfPages - 5">
          <li class="page-item disabled"><a class="page-link">...</a></li>
          <li class="page-item" @click="getPage(numberOfPages)"><a class="page-link">{{numberOfPages}}</a></li>
        </template>

        <li class="page-item" @click="getPage(page+1)" :class="{disabled: page == numberOfPages}"><a class="page-link">Next</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import ImageBox from './components/ImageBox.vue'
  export default {
    name: 'MemeFeed',
    components: {ImageBox},
    data: () => {
      return {
        baseUrl: 'http://127.0.0.1:8000/memes/memes/',
        memes: [],
        count: 0,
        page: 1,
        numberOfPages: 0
      }
    },
    methods: {
      getPage (pageNum) {
        axios.get(this.baseUrl + '?page=' + pageNum)
          .then(response => {
            this.memes = response.data.results
            this.count = response.data.count
            this.page = pageNum
            console.log(this.memes.length)
            this.numberOfPages = this.count / this.memes.length
            console.log(this.memes)
            window.scroll(0, 0)
          })
      }
    },
    created: function () {
      this.getPage(1)
    }
  }
</script>

<style scoped>
  .pagination {
    margin: 0 auto;
  }
</style>
