<template>
  <div class="book-images my-2 container-fluid">
    <Spinner v-if="progress_spinner" />
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
      progress_spinner: false
    };
  },
  asyncComputed: {
    results() {
      this.progress_spinner = true;
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
          this.progress_spinner = false;
          return response.data;
        },
        error => {
          this.progress_spinner = false;
          console.log(error);
        }
      );
    }
  },
  computed: {
    books() {
      if (!!this.results) {
        return this.results.results;
      }
      return [];
    },
    count() {
      if (!!this.results) {
        return this.results.count;
      }
      return 0;
    },
    rest_offset: function() {
      return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    }
  },
  methods: {
    truncate: function(input, length) {
      return input.length > length ? `${input.substring(0, length)}...` : input;
    }
  },
  watch: {
    count() {
      this.$emit("count-update", this.count);
    },
    books() {
      this.$emit("books-update", this.books.length);
    }
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
