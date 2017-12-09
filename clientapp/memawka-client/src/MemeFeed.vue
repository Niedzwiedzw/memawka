<template>
  <div class="container">
    <!--pagination-->
    <div class="container">
      <ul class="pagination pagination-sm justify-content-center">
        <li class="page-item" @click="getPage(page - 1)" :class="{disabled: page == 1}"><a class="page-link"><i class="fa fa-arrow-circle-left"></i></a></li>

        <template
          v-if="page>3">
          <li class="page-item" @click="getPage(1)"><a class="page-link">1</a></li>
          <li class="page-item disabled"><a class="page-link">...</a></li>
        </template>

        <li class="page-item"
            v-for="index in range(page - 2, page + 2)"
            v-if="index <= numberOfPages && index > 0"
            @click="getPage(index)"
            :class="{active:  index == page, 'd-none': index != page, 'd-md-block': true}">
          <a class="page-link">
            {{ index }}
          </a>
        </li>

        <template
          v-if="page < numberOfPages - 1">
          <li class="page-item disabled"><a class="page-link">...</a></li>
          <li class="page-item" @click="getPage(numberOfPages)"><a class="page-link">{{numberOfPages}}</a></li>
        </template>

        <li class="page-item" @click="getPage(page+1)" :class="{disabled: page == numberOfPages}"><a class="page-link"><i class="fa fa-arrow-circle-right"></i></a></li>
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
      <ul class="pagination pagination-sm justify-content-center">
        <li class="page-item" @click="getPage(page - 1)" :class="{disabled: page == 1}"><a class="page-link"><i class="fa fa-arrow-circle-left"></i></a></li>

        <template
          v-if="page>3">
          <li class="page-item" @click="getPage(1)"><a class="page-link">1</a></li>
          <li class="page-item disabled"><a class="page-link">...</a></li>
        </template>

        <li class="page-item"
            v-for="index in range(page - 2, page + 2)"
            v-if="index <= numberOfPages && index > 0"
            @click="getPage(index)"
            :class="{active:  index == page, 'd-none': index != page, 'd-md-block': true}">
          <a class="page-link">
            {{ index }}
          </a>
        </li>

        <template
          v-if="page < numberOfPages - 1">
          <li class="page-item disabled"><a class="page-link">...</a></li>
          <li class="page-item" @click="getPage(numberOfPages)"><a class="page-link">{{numberOfPages}}</a></li>
        </template>

        <li class="page-item" @click="getPage(page+1)" :class="{disabled: page == numberOfPages}"><a class="page-link"><i class="fa fa-arrow-circle-right"></i></a></li>
      </ul>
    </div>
  </div>
</template>

<script>
  import axiosInstance from './http-common'
  export default {
    name: 'MemeFeed',
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
      },
      range (start, end) {
        let list_ = []
        for (let i = start; i < end; i++) {
          list_.push(i)
        }
        return list_
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
