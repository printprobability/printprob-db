<template>
  <div class="container">
    <h2>{{ $route.params.id }} {{ book.title }} - {{ book.estc }}</h2>
    <p>{{ book.n_pages }} pages</p>
    <div class="d-flex flex-wrap justify-content-between">
      <PageImage v-for="page in book.pages" :key="page.pk" :page="page"></PageImage>
    </div>
  </div>
</template>

<script>
import PageImage from "./PageImage.vue";

export default {
  name: "BookDetail",
  components: {
    PageImage
  },
  data: function(d) {
    return {
      book: {}
    };
  },
  methods: {
    get_book: function(id) {
      return axios.get("http://localhost:4000/books/" + id).then(
        response => {
          this.book = response.data;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_book(this.$route.params.id);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.line-image {
}
</style>
