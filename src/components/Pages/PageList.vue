<template>
  <div class="container-fluid">
    <h2>Pages from run {{ page_run.date_started }}</h2>
    <div class="d-flex flex-wrap">
      <PageImage
        v-for="page in page_run.pages"
        :key="page.id"
        :page="page"
        :header="page_header(page)"
      />
    </div>
  </div>
</template>

<script>
import PageImage from "./PageImage";
export default {
  name: "PageList",
  components: {
    PageImage
  },
  props: {
    page_run: Object
  },
  methods: {
    page_header: function(page) {
      return page.spread_sequence + "-" + page.side;
    }
  }
};
</script>

<style scoped>
img.line-image {
  max-width: 800px;
  max-height: 200px;
  border: 2px solid black;
}
</style>
