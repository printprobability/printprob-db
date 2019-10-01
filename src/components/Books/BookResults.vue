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
    <b-list-group class="container">
      <b-list-group-item v-for="book in books" :key="book.eebo">
        <b-media>
          <template v-slot:aside>
            <div class="cover-image-frame">
              <img
                v-if="!!book.cover_spread"
                class="cover-image"
                :src="book.cover_spread.image.web_url"
              />
              <small v-else>No images for this book yet</small>
            </div>
          </template>
          <div class="d-flex justify-content-between">
            <router-link :to="{name: 'BookDetailView', params: {id: book.eebo}}">
              <h5>{{ truncate(book.title, 80) }}</h5>
            </router-link>
            <code>{{ book.eebo }}</code>
          </div>
          <p>{{ book.publisher }}</p>
          <small>
            <a :href="book.pdf">{{ book.pdf }}</a>
          </small>
        </b-media>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
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
    }, 750),
    truncate: function(input, length) {
      return input.length > length ? `${input.substring(0, length)}...` : input;
    }
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

<style scoped>
.cover-image-frame {
  height: 160px;
  width: 160px;
}
img.cover-image {
  display: block;
  max-width: 150px;
  max-height: 150px;
  margin-left: auto;
  margin-right: auto;
}
</style>
