<template>
  <div class="book-images">
    <div class="paginator">
      <p v-show="pagination_needed">Displaying {{ books.length }} out of {{ count }} books</p>
      <b-pagination
        v-show="pagination_needed"
        v-model="page"
        :total-rows="count"
        :per-page="REST_PAGE_SIZE"
        aria-controls="book-results"
      />
    </div>
    <div class="d-flex flex-wrap" id="book-results">
      <BookCover v-for="book in books" :book="book" :key="book.eebo" />
    </div>
  </div>
</template>

<script>
import BookCover from "./BookCover";
import { HTTP, APIConstants } from "../../main";

export default {
  name: "BookResults",
  props: {
    publisher: String
  },
  components: {
    BookCover
  },
  data() {
    return {
      books: [],
      count: null,
      page: 1,
      REST_PAGE_SIZE: APIConstants.REST_PAGE_SIZE
    };
  },
  computed: {
    pagination_needed: function() {
      return this.count > this.REST_PAGE_SIZE;
    },
    rest_offset: function() {
      return (this.page - 1) * this.REST_PAGE_SIZE;
    }
  },
  methods: {
    get_books: function() {
      return HTTP.get("/books/", {
        params: {
          offset: this.rest_offset,
          publisher: this.publisher
        }
      }).then(
        response => {
          this.books = response.data.results;
          this.count = response.data.count;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  watch: {
    publisher: function() {
      this.get_books();
    },
    rest_offset: function() {
      this.get_books();
    }
  },
  created() {
    this.get_books();
  }
};
</script>

<style>
</style>
