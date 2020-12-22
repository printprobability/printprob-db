<template>
  <b-container v-if="book" fluid class="my-3">
    <b-row>
      <b-col cols="6">
        <b-card>
          <template v-slot:header>
            <b-row align-h="between" class="px-3">
              Metadata
              <b-button
                v-if="edit_mode & !readonly"
                variant="danger"
                v-b-modal.delete-modal
                >Delete book</b-button
              >
              <b-modal
                id="delete-modal"
                title="Delete book?"
                ok-variant="danger"
                ok-title="Delete"
                @ok="delete_book"
              >
                <p>
                  Are you sure? This will wipe out every record associated with
                  this book and can't be undone!
                </p>
              </b-modal>
              <b-button
                v-if="edit_mode"
                @click="edit_mode = false"
                variant="warning"
                >Done editing</b-button
              >
              <b-button v-else @click="edit_mode = true" variant="primary"
                >Edit</b-button
              >
            </b-row>
          </template>
          <BookDetailEdit v-if="edit_mode" :book="book" />
          <BookDetailDisplay v-else :book="book" />
        </b-card>
      </b-col>
      <b-col cols="6">
        <b-card header="Components" no-body>
          <b-list-group flush>
            <b-list-group-item>
              <h5>spreads</h5>
              <p
                v-if="book.spreads.length > 0"
                @click="detail_show = 'spreads'"
                class="clickable"
              >
                {{ book.spreads.length }} spreads
              </p>
              <p v-else>No spreads have been loaded for this book yet.</p>
            </b-list-group-item>
            <b-list-group-item
              v-for="(runs, runtype) in book.all_runs"
              :key="runtype"
            >
              <h5>{{ runtype }}</h5>
              <b-table
                class="clickable"
                v-if="runs.length > 0"
                :items="run_table_formatter(runs, runtype)"
                :fields="display_fields"
                primary-key="id"
                small
                bordered
                head-variant="light"
                @row-clicked="select_run"
              >
                <template v-slot:cell(erase)="data">
                  <b-button
                    variant="danger"
                    size="sm"
                    v-b-modal="'delete-modal' + data.item.id"
                    >Delete</b-button
                  >
                  <b-modal
                    :id="'delete-modal' + data.item.id"
                    :title="'Delete this ' + runtype + ' run?'"
                    ok-variant="danger"
                    ok-title="Delete"
                    @ok="run_delete(runtype, data.item.id)"
                    >This will wipe all data from the run, as well as any
                    descendant book components. It cannot be undone.</b-modal
                  >
                </template>
              </b-table>
              <p v-else>No runs for this segmentation type yet.</p>
            </b-list-group-item>
          </b-list-group>
        </b-card>
      </b-col>
    </b-row>
    <SpreadList v-if="detail_show == 'spreads'" :spreads="book.spreads" />
    <PageList v-if="detail_show == 'pages'" :page_run_id="selected_run_id" />
    <LineList
      v-if="detail_show == 'lines'"
      :line_run_id="selected_run_id"
      :n_pages="book.all_runs.pages.slice(-1)[0].component_count"
    />
  </b-container>
</template>

<script>
import BookDetailDisplay from "./BookDetailDisplay";
import BookDetailEdit from "./BookDetailEdit";
import SpreadList from "../Spreads/SpreadList";
import PageList from "../Pages/PageList";
import LineList from "../Lines/LineList";
import moment from "moment";
import { HTTP } from "../../main";

export default {
  name: "BookDetail",
  components: {
    SpreadList,
    PageList,
    LineList,
    BookDetailDisplay,
    BookDetailEdit,
  },
  props: {
    id: String,
  },
  data() {
    return {
      book: null,
      edit_mode: false,
      display_fields: ["date_started", "count", "erase"],
      detail_show: null,
      selected_run: null,
      selected_run_id: null,
    };
  },
  computed: {
    readonly() {
      return this.book.is_eebo_book;
    },
    title_card_header() {
      if (this.readonly) {
        return "Title";
      } else {
        return "Title (click to edit)";
      }
    },
  },
  methods: {
    delete_book: function () {
      this.$root.$bvToast.toast({
        title: `"Deleting ${this.book.pq_title}"`,
        autoHideDelay: 5000,
        appendToast: true,
        variant: "info",
      });
      HTTP.delete("/books/" + this.book.id + "/").then(
        (response) => {
          this.$router.push({ name: "BookListView" });
          this.$root.$bvToast.toast(`"${this.book.pq_title}" deleted`, {
            title: response.data.id,
            autoHideDelay: 5000,
            appendToast: true,
            variant: "success",
          });
        },
        (error) => {
          for (let [k, v] of Object.entries(error.response.data)) {
            this.$bvToast.toast(v, {
              title: error.response.status + ": " + k,
              autoHideDelay: 5000,
              appendToast: true,
              variant: "danger",
            });
          }
        }
      );
    },
    run_delete: function (runtype, id) {
      console.log(runtype + " " + id);
      HTTP.delete("/runs/" + runtype + "/" + id + "/").then(
        (results) => {
          this.get_book(this.id);
          return results;
        },
        (error) => {
          console.log(error);
        }
      );
    },
    get_book: function (id) {
      return HTTP.get("/books/" + id + "/").then(
        (response) => {
          this.book = response.data;
        },
        (error) => {
          console.log(error);
        }
      );
    },
    display_date: function (date) {
      return moment(new Date(date)).format("MM-DD-YY, h:mm a");
    },
    run_table_formatter: function (run, runtype) {
      return run.map((r) => {
        return {
          id: r.id,
          type: runtype,
          date_started: this.display_date(r.date_started),
          count: r.component_count,
        };
      });
    },
    select_run: function (payload) {
      const run_type = payload.type;
      const run_id = payload.id;
      if (run_type == "characters") {
        this.$router.push({
          name: "CharacterGroupingView",
          query: { book: this.book.id, character_run: run_id },
        });
      } else if (run_type == "lines") {
        this.detail_show = run_type;
        this.selected_run_id = run_id;
      } else {
        return HTTP.get("/runs/" + run_type + "/" + run_id + "/").then(
          (response) => {
            this.selected_run = response.data;
            this.selected_run_id = run_id;
            this.detail_show = run_type;
          },
          (error) => {
            console.log(error);
          }
        );
      }
    },
  },
  created: function () {
    this.get_book(this.id);
  },
};
</script>

<style scoped>
.clickable {
  cursor: pointer;
}
</style>
