<template>
  <b-container fluid>
    <b-row align-h="between">
      <div class="paginator">
        <p>
          Displaying books {{ page_range[0].toLocaleString() }} to
          {{ page_range[1].toLocaleString() }} out of
          {{ count.toLocaleString() }} total
        </p>
        <b-pagination
          hide-goto-end-buttons
          v-model="page"
          :total-rows="count"
          :per-page="$APIConstants.BOOK_PAGE_SIZE"
          aria-controls="book-results"
        />
      </div>
      <b-spinner v-show="fetch_state == 'getting'" />
      <b-form-group id="sort-group" label-for="sort-select" label="Sort">
        <BookSort v-model="order" />
      </b-form-group>
    </b-row>
    <b-list-group>
      <b-list-group-item v-for="book in books" :key="book.id">
        <BookResultCard :book="book" />
      </b-list-group-item>
    </b-list-group>
    <b-pagination
      hide-goto-end-buttons
      v-model="page"
      :total-rows="count"
      :per-page="$APIConstants.BOOK_PAGE_SIZE"
      aria-controls="book-results"
    />
  </b-container>
</template>

<script>
import { HTTP } from "../../main";
import BookSort from "../Menus/BookSort";
import BookResultCard from "./BookResultCard";

export default {
  name: "BookResults",
  components: {
    BookSort,
    BookResultCard,
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
    year_early: String,
    year_late: String,
    starred: Boolean,
    pp_publisher: String,
    pp_author: String,
    pp_printer: String,
    colloq_printer: String,
    pp_repository: String,
  },
  data() {
    return {
      fetch_state: "waiting",
      order: "pq_title",
      page: 1,
    };
  },
  asyncComputed: {
    results() {
      this.fetch_state = "getting";
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
          year_early_min: this.year_early,
          year_late_max: this.year_late,
          pp_publisher: this.pp_publisher,
          pp_author: this.pp_author,
          repository: this.pp_repository,
          pp_printer: this.pp_printer,
          colloq_printer: this.colloq_printer,
          starred: this.starred,
          ordering: this.order,
        },
      }).then(
        (response) => {
          this.fetch_state = "done";
          return response.data;
        },
        (error) => {
          this.fetch_state = "done";
          console.log(error);
        }
      );
    },
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
    results_length() {
      if (!!this.results) {
        return this.results.results.length;
      }
      return 0;
    },
    rest_offset: function () {
      return (this.page - 1) * this.$APIConstants.BOOK_PAGE_SIZE;
    },
    page_range: function () {
      var base = 0;
      if (this.page > 1) {
        base = (this.page - 1) * this.$APIConstants.BOOK_PAGE_SIZE;
      }
      return [base + 1, this.results_length + base];
    },
    view_params() {
      return {
        eebo: this.eebo,
        pq_publisher: this.publisher_search,
        pq_title: this.title_search,
        pq_author: this.author_search,
        pp_publisher: this.pp_publisher_search,
        pp_printer: this.pp_printer_search,
        colloq_printer: this.colloq_printer,
        pp_repository: this.pp_repository_search,
        pq_year_min: this.pq_year_min,
        pq_year_max: this.pq_year_max,
        year_late_max: this.year_early,
        year_early_min: this.year_late,
        order: this.order,
      };
    },
  },
  watch: {
    view_params: function () {
      this.page = 1;
    },
  },
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
