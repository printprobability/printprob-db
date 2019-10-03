<template>
  <div class="container">
    <router-link v-if="page.book" :to="{name: 'BookDetailView', params: {id: page.book.id}}">
      <h2>{{ $route.params.id }} - {{ page.book.pq_publisher }} - page {{ page.spread_sequence }} {{ page.side }}</h2>
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
      <li v-for="line in page.most_recent_lines" :key="line.id">
        <LineImage :line="line"></LineImage>
      </li>
    </ol>
  </div>
</template>

<script>
import LineImage from "../Lines/LineImage";

export default {
  name: "PageDetail",
  components: {
    LineImage
  },
  props: {
    page: Object
  },
  data() {
    return {};
  },
  methods: {}
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
