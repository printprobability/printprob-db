<template>
  <div class="container-fluid">
    <div class="card my-2">
      <div class="card-header">Filter books</div>
      <div class="card-body">
        <b-row>
          <b-col col lg="6" class="border-right p-3">
            <h5>EEBO metadata</h5>
            <b-form-row>
              <b-col col md="6">
                <b-form-group
                  id="publisher-group"
                  label="Publisher"
                  label-for="publisher-input"
                  description="Partial publisher name (case insensitive)"
                >
                  <b-form-input
                    id="publisher-input"
                    v-model="publisher_search"
                    placeholder="overton"
                  />
                </b-form-group>
                <b-form-group
                  id="title-group"
                  label-for="title-input"
                  label="Title"
                  description="Search by partial title (case insensitive)"
                >
                  <b-form-input
                    id="title-input"
                    v-model="title_search"
                    placeholder="nine arguments"
                  />
                </b-form-group>
              </b-col>
              <b-col col md="6">
                <b-form-group
                  id="author-group"
                  label-for="author-input"
                  label="Author"
                  description="Search by partial author (case insensitive)"
                >
                  <b-form-input id="author-input" v-model="author_search" placeholder="milton" />
                </b-form-group>
                <b-form-group
                  id="pq_year_group"
                  label-for="pq_year_input"
                  label="Year"
                  description="Get books produced within this year range"
                >
                  <vue-slider
                    id="pq_year_input"
                    v-model="pq_year_range"
                    tooltip="always"
                    tooltip-placement="bottom"
                    :enable-cross="false"
                    :min="min_year"
                    :max="max_year"
                  />
                </b-form-group>
                <b-form-group
                  id="tx_year_group"
                  label-for="tx_year_input"
                  label="Texas A&M Year"
                  description="Get books produced within this year range"
                >
                  <vue-slider
                    v-model="tx_year_range"
                    tooltip="always"
                    tooltip-placement="bottom"
                    :enable-cross="false"
                    :min="min_year"
                    :max="max_year"
                  />
                </b-form-group>
              </b-col>
            </b-form-row>
          </b-col>
          <b-col col lg="6" class="p-3">
            <h5>P&P metadata</h5>
            <b-form-row>
              <b-col col md="6">
                <b-form-group
                  id="pp-publisher-group"
                  label="Publisher"
                  description="Search by partial publisher (as assigned by P&P)"
                >
                  <b-form-input
                    id="pp-publisher-input"
                    v-model="pp_publisher_search"
                    placeholder="simmons"
                  />
                </b-form-group>
                <b-form-group id="book-image-group" label="Only show books with images">
                  <b-form-checkbox id="book-image-input" v-model="has_images" />
                </b-form-group>
              </b-col>
              <b-col col md="6">
                <b-form-group
                  id="date-range-group"
                  label="Books published between"
                  description="Only books whose dates overlap the specified range"
                >
                  <b-form inline>
                    <b-form-input
                      class="mx-2"
                      id="year-input-early"
                      type="date"
                      v-model="year_early"
                    />and
                    <b-form-input
                      class="mx-2"
                      id="year-input-late"
                      type="date"
                      v-model="year_late"
                    />
                  </b-form>
                </b-form-group>
              </b-col>
            </b-form-row>
          </b-col>
        </b-row>
      </div>
    </div>
    <b-container fluid>
      <b-row align-h="between">
        <div class="paginator">
          <p>Displaying books {{ page_range[0].toLocaleString() }} to {{ page_range[1].toLocaleString() }} out of {{ count.toLocaleString() }} total</p>
          <b-pagination
            hide-goto-end-buttons
            v-model="page"
            :total-rows="count"
            :per-page="$APIConstants.REST_PAGE_SIZE"
            aria-controls="book-results"
          />
        </div>
        <b-spinner v-show="fetch_state=='getting'" />
        <b-form-group id="sort-group" label-for="sort-select" label="Sort">
          <BookSort v-model="order" />
        </b-form-group>
      </b-row>
      <BookResults
        :publisher="publisher_search"
        :title="title_search"
        :author="author_search"
        :year_early="year_early"
        :year_late="year_late"
        :pq_year_min="pq_year_range[0]"
        :pq_year_max="pq_year_range[1]"
        :tx_year_min="tx_year_range[0]"
        :tx_year_max="tx_year_range[1]"
        :has_images="has_images"
        :pp_publisher="pp_publisher_search"
        :page="page"
        :order="order"
        @count-update="count=$event"
        @books-update="results_length=$event"
        @state="fetch_state=$event"
      />
    </b-container>
  </div>
</template>

<script>
import BookResults from "./BookResults";
import BookSort from "../Menus/BookSort";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

export default {
  name: "BookList",
  components: {
    BookResults,
    BookSort,
    VueSlider
  },
  data() {
    return {
      min_year: 1500,
      max_year: 1800,
      publisher_search: "",
      title_search: "",
      author_search: "",
      pp_publisher_search: "",
      pq_year_range: [1500, 1800],
      tx_year_range: [1500, 1800],
      year_early: null,
      year_late: null,
      has_images: false,
      page: 1,
      order: "pq_title",
      count: 0,
      results_length: 0,
      fetch_state: "waiting"
    };
  },
  computed: {
    view_params() {
      return {
        pq_publisher: this.publisher_search,
        pq_title: this.title_search,
        pq_author: this.author_search,
        pp_publisher: this.pp_publisher_search,
        pq_year_min: this.pq_year_range[0],
        pq_year_max: this.pq_year_range[1],
        tx_year_min: this.tx_year_range[0],
        tx_year_max: this.tx_year_range[1],
        year_late_max: this.year_early,
        year_early_min: this.year_late,
        has_images: this.has_images,
        page: this.page,
        order: this.order
      };
    },
    page_range: function() {
      var base = 0;
      if (this.page > 1) {
        base = (this.page - 1) * this.$APIConstants.BOOK_PAGE_SIZE;
      }
      return [base + 1, this.results_length + base];
    }
  },
  created() {
    var pn = !!this.$route.query.page ? Number(this.$route.query.page) : 1;

    this.publisher_search = this.$route.query.pq_publisher;
    this.title = this.$route.query.pq_title;
    this.author = this.$route.query.pq_author;
    this.pp_publisher = this.$route.query.pp_publisher;
    this.has_images = this.$route.query.has_images == "true";
    this.year_early = this.$route.query.date_early;
    this.year_late = this.$route.query.date_late;
    this.page = Number(pn);
  },
  updated() {
    this.$router.push({ name: "BookListView", query: this.view_params });
  }
};
</script>

<style scoped>
.vue-slider {
  margin: 0em 1em 2em 1em;
}
</style>