<template>
  <b-list-group>
    <b-list-group-item v-for="book in books" :key="book.id">
      <BookResultCard :book="book" />
    </b-list-group-item>
  </b-list-group>
</template>

<script>
import { HTTP } from "../../main";
import BookResultCard from "./BookResultCard";

export default {
  name: "BookResults",
  components: {
    BookResultCard
  },
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
    starred: Boolean,
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
          starred: this.starred,
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
  methods: {},
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
