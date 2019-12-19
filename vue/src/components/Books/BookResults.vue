<template>
  <b-list-group>
    <b-list-group-item v-for="book in books" :key="book.id">
      <b-media>
        <template v-slot:aside>
          <div class="cover-image-frame">
            <img
              v-if="!!book.cover_spread"
              class="cover-image"
              :src="book.cover_spread.image.thumbnail"
            />
            <small v-else>Not run yet</small>
          </div>
        </template>
        <router-link :to="{name: 'BookDetailView', params: {id: book.id}}">
          <h5>{{ truncate(book.pq_title, 140) }}</h5>
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
            <p>
              EEBO ID:
              <code>{{ book.eebo }}</code>
            </p>
            <p>
              VID:
              <code>{{ book.vid }}</code>
            </p>
            <p>
              Bridges zipfile:
              <code>{{ book.zipfile }}</code>
              <br />
              <code>unzip -d . {{ book.zipfile }}.zip {{ book.zipfile }}/{{ book.vid }}/*</code>
            </p>
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
</template>

<script>
import { HTTP } from "../../main";

export default {
  name: "BookResults",
  props: {
    publisher: String,
    eebo: Number,
    vid: Number,
    tcp: String,
    estc: String,
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
  data() {
    return {
      state: "waiting"
    };
  },
  asyncComputed: {
    results() {
      this.state = "getting";
      return HTTP.get("/books/", {
        params: {
          limit: this.$APIConstants.BOOK_PAGE_SIZE,
          offset: this.rest_offset,
          eebo: this.eebo,
          vid: this.vid,
          tcp: this.tcp,
          estc: this.estc,
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
          this.state = "done";
          return response.data;
        },
        error => {
          this.state = "done";
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
    },
    state() {
      this.$emit("state", this.state);
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
