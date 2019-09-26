<template>
  <div v-if="book" class="container-fluid">
    <div class="row">
      <div class="col-4">
        <div class="card my-2">
          <div class="card-header">EEBO Metadata</div>
          <div class="card-body">
            <router-link :to="{name: 'BookDetailView', params: {id: book.eebo}}">
              <h4>{{ book.title }}</h4>
            </router-link>
            <p>Published by: {{ book.publisher }}</p>
            <p>EEBO id: {{ book.eebo }}</p>
            <p @click="detail_show='spreads'">{{ book.n_spreads }} Spreads</p>
          </div>
        </div>
      </div>
      <div class="col-8">
        <div class="card my-2">
          <div class="card-header">Bridges Jobs</div>
          <b-list-group flush>
            <b-list-group-item v-for="(runs, runtype) in book.all_runs" :key="runtype">
              <h5>{{ runtype }}</h5>
              <b-table
                v-if="runs.length > 0"
                :items="run_table_formatter(runs, runtype)"
                :fields="display_fields"
                primary-key="id"
                small
                bordered
                head-variant="light"
                @row-clicked="select_run"
              />
              <p v-else>No runs for this segmentation type yet.</p>
            </b-list-group-item>
          </b-list-group>
        </div>
      </div>
    </div>
    <SpreadList v-if="detail_show=='spreads'" :spreads="book.spreads" />
    <PageList v-if="detail_show=='pages'" :page_run="selected_run" />
    <CharacterList
      v-if="detail_show=='characters'"
      :initial_values="{page: 1, character_class: null, book: book.eebo}"
    />
  </div>
</template>

<script>
import SpreadList from "../Spreads/SpreadList";
import PageList from "../Pages/PageList";
import CharacterList from "../Characters/CharacterList";
import moment from "moment";
import { HTTP } from "../../main";

export default {
  name: "BookDetail",
  components: {
    SpreadList,
    PageList,
    CharacterList
  },
  props: {
    id: Number
  },
  data() {
    return {
      book: null,
      display_fields: ["count", "date_started"],
      detail_show: "spreads",
      selected_run: null
    };
  },
  methods: {
    get_book: function(id) {
      HTTP.get("/books/" + id + "/").then(
        response => {
          this.book = response.data;
        },
        error => {
          console.log(error);
        }
      );
    },
    display_date: function(date) {
      return moment(new Date(date)).format("MM-DD-YY, h:mm a");
    },
    run_table_formatter: function(run, runtype) {
      return run.map(r => {
        return {
          id: r.id,
          type: runtype,
          count: r[runtype].length,
          date_started: this.display_date(r.date_started)
        };
      });
    },
    select_run: function(payload) {
      const run_type = payload.type;
      const run_id = payload.id;
      return HTTP.get("/runs/" + run_type + "/" + run_id + "/").then(
        response => {
          this.selected_run = response.data;
          this.detail_show = run_type;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  created: function() {
    this.get_book(this.id);
  }
};
</script>
