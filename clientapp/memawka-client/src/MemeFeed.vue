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
  import axiosInstance from './http-common'
  import ImageBox from './components/ImageBox.vue'
  export default {
    name: 'MemeFeed',
    components: {ImageBox},
    data: () => {
      return {
        baseUrl: 'memes/memes/',
        memes: [],
        count: 0,
        page: 1,
        numberOfPages: 0
      }
    },
    methods: {
      getPage (pageNum) {
        axiosInstance.get(this.baseUrl + '?page=' + pageNum)
          .then(response => {
            this.memes = response.data.results
            this.count = response.data.count
            this.page = pageNum
            this.numberOfPages = Math.ceil(this.count / 10)
            window.scroll(0, 0)
          })
      }
    },
    mounted: function () {
      this.getPage(1)
    }
  }
</script>

<style scoped>
  .pagination {
    margin: 0 auto;
  }
</style>
