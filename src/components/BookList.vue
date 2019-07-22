<template>
  <div id="app">
    <h1>All Books</h1>
    <div class="book-covers card-columns">
      <BookCover v-for="book in books" :book="book" :key="book.eebo" />
    </div>
  </div>
</template>

<script>
import BookCover from "./BookCover.vue";
import axios from "axios";

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

export default {
  name: "BookList",
  components: {
    BookCover
  },
  data: function(d) {
    return {
      books: [],
      pagination: {
        count: null,
        next: null,
        previous: null
      }
    };
  },
  methods: {
    get_books: function() {
      return axios.get("http://localhost/books/").then(
        response => {
          this.books = response.data.results;
          this.pagination.count = response.data.count;
          this.pagination.next = response.data.next;
          this.pagination.previous = response.data.previous;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_books();
  }
};
</script>

<style>
</style>
