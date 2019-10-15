<template>
  <div class="container-fluid">
    <div class="card my-2">
      <div class="card-header">Filter books</div>
      <div class="card-body">
        <h5>EEBO metadata</h5>
        <b-row>
          <div class="col-4">
            <b-form-group
              id="publisher-group"
              label="Publisher"
              label-for="publisher-input"
              description="Partial publisher name (case insensitive)"
            >
              <b-form-input id="publisher-input" v-model="publisher_search" placeholder="overton" />
            </b-form-group>
          </div>
          <div class="col-4">
            <b-form-group
              id="title-group"
              label-for="title-input"
              label="Title"
              description="Search by partial title (case insensitive)"
            >
              <b-form-input id="title-input" v-model="title_search" placeholder="nine arguments" />
            </b-form-group>
          </div>
          <div class="col-4">
            <b-form-group
              id="author-group"
              label-for="author-input"
              label="Author"
              description="Search by partial author (case insensitive)"
            >
              <b-form-input id="author-input" v-model="author_search" placeholder="milton" />
            </b-form-group>
          </div>
        </b-row>

        <h5>P&P metadata</h5>
        <b-row>
          <b-col cols="4">
            <b-form-group
              id="pp-publisher-group"
              label="Search by partial publisher (as assigned by P&P)"
            >
              <b-form-input
                id="pp-publisher-input"
                v-model="pp_publisher_search"
                placeholder="simmons"
              />
            </b-form-group>
          </b-col>
          <b-col cols="4">
            <b-form-group id="book-image-group" label="Only show books with images">
              <b-form-checkbox id="book-image-input" v-model="has_images" />
            </b-form-group>
          </b-col>
          <b-col cols="4">
            <b-form-group
              id="date-range-group"
              label="Books published between"
              description="Only books whose dates are wholly within the specified range"
            >
              <b-form inline>
                <b-form-input
                  class="mx-2"
                  size="sm"
                  id="year-input-early"
                  type="date"
                  v-model="year_early"
                />and
                <b-form-input
                  class="mx-2"
                  size="sm"
                  id="year-input-late"
                  type="date"
                  v-model="year_late"
                />
              </b-form>
            </b-form-group>
          </b-col>
        </b-row>
      </div>
    </div>
    <BookResults
      :publisher="publisher_search"
      :title="title_search"
      :author="author_search"
      :year_early="year_early"
      :year_late="year_late"
      :has_images="has_images"
      :pp_publisher="pp_publisher_search"
      :page="page"
      @update_page="page=$event"
    />
  </div>
</template>

<script>
import BookResults from "./BookResults";

export default {
  name: "BookList",
  components: {
    BookResults
  },
  data() {
    return {
      publisher_search: "",
      title_search: "",
      author_search: "",
      pp_publisher_search: "",
      year_early: null,
      year_late: null,
      has_images: false,
      page: 1
    };
  },
  computed: {
    view_params() {
      return {
        pq_publisher: this.publisher_search,
        pq_title: this.title_search,
        pq_author: this.author_search,
        pp_publisher: this.pp_publisher_search,
        year_early: this.year_early,
        year_late: this.year_late,
        has_images: this.has_images,
        page: this.page
      };
    }
  },
  created() {
    var pn = !!this.$route.query.page ? Number(this.$route.query.page) : 1;

    this.publisher_search = this.$route.query.pq_publisher;
    this.title = this.$route.query.pq_title;
    this.author = this.$route.query.pq_author;
    this.pp_publisher = this.$route.query.pp_publisher;
    this.has_images = this.$route.query.has_images;
    this.year_early = this.$route.query.date_early;
    this.year_late = this.$route.query.date_late;
    this.page = pn;
  },
  updated() {
    this.$router.push({ name: "BookListView", query: this.view_params });
  }
};
</script>
