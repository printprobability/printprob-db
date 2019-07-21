<template>
  <div class="container">
    <router-link v-if="page.book" :to="{name: 'BookDetailView', params: {id: page.book}}">
      <h2>{{ $route.params.id }} {{ page.book_title }} - page {{ page.sequence }} {{ page.side }}</h2>
    </router-link>
    <div class="button-pagination d-flex justify-content-between">
      <button
        :disabled="!page.previous_page"
        class="btn btn-primary"
        role="button"
        @click="$router.push({ name: 'PageDetailView', params: { id: page.previous_page } })"
      >Previous</button>
      <button
        :disabled="!page.next_page"
        class="btn btn-primary"
        role="button"
        @click="$router.push({ name: 'PageDetailView', params: { id: page.next_page } })"
      >Next</button>
    </div>
    <ol>
      <li v-for="line in page.lines" :key="line.pk">
        <LineImage :line="line"></LineImage>
      </li>
    </ol>
  </div>
</template>

<script>
import LineImage from "./LineImage.vue";
import axios from "axios";

export default {
  name: "PageDetail",
  components: {
    LineImage
  },
  data: function(d) {
    return {
      page: {}
    };
  },
  methods: {
    get_page: function(id) {
      return axios.get("http://localhost/pages/" + id).then(
        response => {
          this.page = response.data;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_page(this.$route.params.id);
  },
  watch: {
    $route(to, from) {
      this.get_page(this.$route.params.id);
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
