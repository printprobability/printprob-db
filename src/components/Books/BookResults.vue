<template>
  <div class="book-images my-2">
    <Spinner v-if="progress_spinner" />
    <div class="paginator">
      <p v-show="pagination_needed">Displaying {{ books.length }} out of {{ count }} books</p>
      <b-pagination
        v-show="pagination_needed"
        v-model="page"
        :total-rows="count"
        :per-page="$APIConstants.REST_PAGE_SIZE"
        aria-controls="book-results"
      />
    </div>
    <div class="d-flex flex-wrap" id="book-results">
      <SpreadImage
        class="mr-2"
        v-for="book in books"
        :key="book.eebo"
        :spread="book.cover_spread"
        :header="book.publisher + ': ' + book.title"
        :footer="'EEBO: ' + book.eebo"
        :link="{name: 'BookDetailView', params: {id: book.eebo}}"
      />
    </div>
  </div>
</template>

<script>
import SpreadImage from "../Spreads/SpreadImage";
import Spinner from "../Interfaces/Spinner";
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "BookResults",
  props: {
    publisher: String,
    title: String
  },
  components: {
    SpreadImage,
    Spinner
  },
  data() {
    return {
      books: [],
      count: null,
      page: 1,
      progress_spinner: false
    };
  },
  computed: {
    pagination_needed: function() {
      return this.count > this.$APIConstants.REST_PAGE_SIZE;
    },
    rest_offset: function() {
      return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    }
  },
  methods: {
    get_books: function() {
      return HTTP.get("/books/", {
        params: {
          offset: this.rest_offset,
          publisher: this.publisher,
          title: this.title
        }
      }).then(
        response => {
          this.books = response.data.results;
          this.count = response.data.count;
          this.progress_spinner = false;
        },
        error => {
          console.log(error);
        }
      );
    },
    debounced_get_books: _.debounce(function() {
      this.get_books();
    }, 750)
  },
  watch: {
    publisher: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    title: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    rest_offset: function() {
      this.progress_spinner = true;
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
