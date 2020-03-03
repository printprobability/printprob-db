<template>
  <div class="container-fluid">
    <div class="card my-2">
      <div class="card-header">
        <b-row align-v="center" align-h="between">
          <span class="ml-2">Filter books</span>
          <b-button variant="success" :to="{name: 'BookCreateView'}">Create book</b-button>
        </b-row>
      </div>
      <div class="card-body">
        <b-form-row>
          <b-col col lg="6" class="border-right p-3">
            <h5>EEBO metadata</h5>
            <b-form-row>
              <b-col col md="6">
                <b-form-group
                  id="eebo-group"
                  label="EEBO id"
                  label-for="eebo-input"
                  label-size="sm"
                >
                  <b-form-input
                    size="sm"
                    id="eebo-input"
                    v-model="eebo_search"
                    placeholder="99896497"
                    type="number"
                    number
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group id="vid-group" label="VID" label-for="vid-input" label-size="sm">
                  <b-form-input
                    number
                    type="number"
                    size="sm"
                    id="vid-input"
                    v-model="vid_search"
                    placeholder="184449"
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group id="tcp-group" label="tcp" label-for="tcp-input" label-size="sm">
                  <b-form-input
                    size="sm"
                    id="tcp-input"
                    v-model="tcp_search"
                    placeholder="A27900"
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group id="estc-group" label="estc" label-for="estc-input" label-size="sm">
                  <b-form-input
                    size="sm"
                    id="estc-input"
                    v-model="estc_search"
                    placeholder="R23698"
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group
                  id="publisher-group"
                  label="Publisher"
                  label-for="publisher-input"
                  description="Partial publisher name (case insensitive)"
                  label-size="sm"
                >
                  <b-form-input
                    size="sm"
                    id="publisher-input"
                    v-model="publisher_search"
                    placeholder="overton"
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group
                  id="title-group"
                  label-for="title-input"
                  label="Title"
                  description="Search by partial title (case insensitive)"
                  label-size="sm"
                >
                  <b-form-input
                    size="sm"
                    id="title-input"
                    v-model="title_search"
                    placeholder="nine arguments"
                    debounce="750"
                  />
                </b-form-group>
              </b-col>
              <b-col col md="6">
                <b-form-group
                  id="author-group"
                  label-for="author-input"
                  label="Author"
                  description="Search by partial author (case insensitive)"
                  label-size="sm"
                >
                  <b-form-input
                    size="sm"
                    id="author-input"
                    v-model="author_search"
                    placeholder="milton"
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group
                  id="pq_year_group"
                  label-for="pq_year_input"
                  label="Year"
                  description="Get books produced within this year range"
                  label-size="sm"
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
                  label-size="sm"
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
                  label-size="sm"
                >
                  <b-form-input
                    size="sm"
                    id="pp-publisher-input"
                    v-model="pp_publisher_search"
                    placeholder="simmons"
                    debounce="750"
                  />
                </b-form-group>
                <b-form-group id="starred-group" label="Only show starred books" label-size="sm">
                  <b-form-checkbox
                    id="starred-input"
                    v-model="starred"
                    checked-value="true"
                    unchecked-value="null"
                  />
                </b-form-group>
              </b-col>
              <b-col col md="6">
                <b-form-group
                  id="date-range-group"
                  label="Books published between"
                  description="Only books whose dates overlap the specified range"
                  label-size="sm"
                >
                  <b-form inline>
                    <b-form-input
                      size="sm"
                      class="mx-2"
                      id="year-input-early"
                      type="date"
                      v-model="year_early"
                      debounce="750"
                    />and
                    <b-form-input
                      size="sm"
                      class="mx-2"
                      id="year-input-late"
                      type="date"
                      v-model="year_late"
                      debounce="750"
                    />
                  </b-form>
                </b-form-group>
              </b-col>
            </b-form-row>
          </b-col>
        </b-form-row>
      </div>
    </div>
    <BookResults
      :eebo="eebo_search"
      :vid="vid_search"
      :tcp="tcp_search"
      :estc="estc_search"
      :publisher="publisher_search"
      :title="title_search"
      :author="author_search"
      :year_early="year_early"
      :year_late="year_late"
      :pq_year_min="pq_year_min"
      :pq_year_max="pq_year_max"
      :tx_year_min="tx_year_min"
      :tx_year_max="tx_year_max"
      :starred="starred"
      :pp_publisher="pp_publisher_search"
    />
  </div>
</template>

<script>
import BookResults from "./BookResults";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";
import _ from "lodash";

export default {
  name: "BookList",
  components: {
    BookResults,
    VueSlider
  },
  data() {
    return {
      min_year: 1500,
      max_year: 1800,
      eebo_search: null,
      vid_search: null,
      tcp_search: null,
      estc_search: null,
      publisher_search: "",
      title_search: "",
      author_search: "",
      pp_publisher_search: "",
      pq_year_range: [1500, 1800],
      pq_year_min: 1500,
      pq_year_max: 1800,
      tx_year_range: [1500, 1800],
      tx_year_min: 1500,
      tx_year_max: 1800,
      year_early: null,
      year_late: null,
      starred: null
    };
  },
  watch: {
    pq_year_range: _.debounce(function() {
      this.pq_year_min = this.pq_year_range[0];
      this.pq_year_max = this.pq_year_range[1];
    }, 750),
    tx_year_range: _.debounce(function() {
      this.tx_year_min = this.tx_year_range[0];
      this.tx_year_max = this.tx_year_range[1];
    }, 750)
  }
};
</script>

<style scoped>
.vue-slider {
  margin: 0em 1em 2em 1em;
}
</style>