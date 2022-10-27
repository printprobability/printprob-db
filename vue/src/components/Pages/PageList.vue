<template>
  <div class="container-fluid">
    <div class="d-flex flex-wrap">
      <PageImage
        v-for="page in pages"
        :key="page.id"
        :page="page"
        :header="page_header(page)"
      />
    </div>
  </div>
</template>

<script>
import PageImage from './PageImage'
import { HTTP } from '../../main'
export default {
  name: 'PageList',
  components: {
    PageImage,
  },
  props: {
    page_run_id: String,
  },
  methods: {
    page_header: function (page) {
      return page.sequence
    },
  },
  asyncComputed: {
    pages() {
      return HTTP.get('/pages/', {
        params: {
          created_by_run: this.page_run_id,
          limit: 2000,
        },
      }).then(
        (response) => {
          return response.data.results
        },
        (error) => {
          console.log(error)
        }
      )
    },
  },
}
</script>

<style scoped>
img.line-image {
  max-width: 800px;
  max-height: 200px;
  border: 2px solid black;
}
</style>
