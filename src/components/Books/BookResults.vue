<template>
  <div class="book-images my-2 container-fluid">
    <Spinner v-if="progress_spinner" />
    <b-row align-h="between">
      <div class="paginator">
        <p v-show="pagination_needed">Displaying {{ books.length }} out of {{ count }} books</p>
        <b-pagination
          hide-goto-end-buttons
          v-show="pagination_needed"
          v-model="page"
          :total-rows="count"
          :per-page="$APIConstants.REST_PAGE_SIZE"
          aria-controls="book-results"
        />
      </div>
      <b-form-group id="sort-group" label-for="sort-select" label="Sort">
        <b-form-select id="sort-select" v-model="order" :options="sort_options" />
      </b-form-group>
    </b-row>
    <b-list-group>
      <b-list-group-item v-for="book in books" :key="book.id">
        <b-media>
          <template v-slot:aside>
            <div class="cover-image-frame">
              <img
                v-if="!!book.cover_spread"
                class="cover-image"
                :src="book.cover_spread.image.web_url"
              />
              <small v-else>Not run yet</small>
            </div>
          </template>
          <router-link :to="{name: 'BookDetailView', params: {id: book.id}}">
            <h5>{{ truncate(book.pq_title, 80) }}</h5>
          </router-link>
          <b-row class="mt-3">
            <b-col cols sm="6" class="border-right">
              <p class="bg-light p-2">EEBO / ProQuest</p>
              <small>
                <a :href="book.pq_url">{{ book.pq_url }}</a>
              </small>
              <p>Author: {{ book.pq_author }}</p>
              <p>Publisher: {{ book.pq_publisher }}</p>
              <p>EEBO date: {{ book.pq_year_early }}-{{ book.pq_year_late }}</p>
              <p>TX A&M date: {{ book.tx_year_early }}-{{ book.tx_year_late }}</p>
            </b-col>
            <b-col cols sm="6">
              <p class="bg-light p-2">P&P</p>
              <p>Date between: {{ book.date_early }} and {{ book.date_late }}</p>
              <p>Publisher: {{ book.pp_publisher }}</p>
            </b-col>
          </b-row>
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
    title: String,
    author: String,
    pq_year_min: Number,
    pq_year_max: Number,
    tx_year_min: Number,
    tx_year_max: Number,
    year_early: String,
    year_late: String,
    has_images: Boolean,
    pp_publisher: String,
    order: {
      type: String,
      default: "pq_title"
    },
    page: {
      type: Number,
      default: 1
    }
  },
  components: {
    Spinner
  },
  data() {
    return {
      books: [],
      count: null,
      progress_spinner: false
    };
  },
  computed: {
    pagination_needed: function() {
      return this.count > this.$APIConstants.REST_PAGE_SIZE;
    },
    rest_offset: function() {
      return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    },
    sort_options() {
      return [
        { text: "Title A-Z", value: "pq_title" },
        { text: "Title Z-A", value: "-pq_title" },
        { text: "Author A-Z", value: "pq_author" },
        { text: "Author Z-A", value: "-pq_author" },
        { text: "Publisher A-Z", value: "pq_publisher" },
        { text: "Publisher Z-A", value: "-pq_publisher" },
        { text: "Oldest first", value: "date_early" },
        { text: "Recent first", value: "date_early" }
      ];
    }
  },
  methods: {
    get_books: function() {
      return HTTP.get("/books/", {
        params: {
          limit: 25,
          offset: this.rest_offset,
          pq_publisher: this.publisher,
          pq_title: this.title,
          pq_author: this.author,
          pq_year_early_min: this.pq_year_min,
          pq_year_late_max: this.pq_year_max,
          tx_year_early_min: this.tx_year_min,
          tx_year_late_max: this.tx_year_max,
          year_early_min: this.year_early,
          year_late_max: this.year_late,
          images: this.has_images,
          pp_publisher: this.pp_publisher,
          ordering: this.order
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
    author: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    pq_year_min: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    pq_year_max: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    tx_year_min: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    tx_year_max: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    year_early: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    year_late: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    has_images: function() {
      this.progress_spinner = true;
      this.get_books();
    },
    pp_publisher: function() {
      this.progress_spinner = true;
      this.debounced_get_books();
    },
    rest_offset: function() {
      this.progress_spinner = true;
      this.get_books();
    },
    page() {
      this.$emit("update_page", this.page);
    },
    order() {
      this.progress_spinner = true;
      this.get_books();
      this.$emit("update_order", this.order);
    }
  },
  created() {
    this.progress_spinner = true;
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
