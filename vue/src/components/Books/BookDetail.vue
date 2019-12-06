<template>
  <div v-if="book" class="container-fluid">
    <div class="row">
      <div class="col-6">
        <div class="card my-2">
          <div class="card-header">EEBO Metadata</div>
          <div class="card-body">
            <h5>{{ book.pq_title }}</h5>
            <p>Publisher: {{ book.pq_publisher }}</p>
            <p>Author: {{ book.pq_author }}</p>
            <p>
              EEBO id:
              <code>{{ book.eebo }}</code>
            </p>
            <p>
              VID:
              <code>{{ book.vid }}</code>
            </p>
            <p>
              Proquest link:
              <a :href="book.pq_url">{{ book.pq_url }}</a>
            </p>
          </div>
        </div>
        <div class="card my-2">
          <div class="card-header">P&P Metadata</div>
          <div class="card-body">
            <p>
              UUID:
              <code>{{ book.id }}</code>
            </p>

            <dl class="row">
              <dt class="col-sm-3">Publisher</dt>
              <dd
                class="col-sm-9"
                contenteditable="contenteditable"
                @blur="edit_group('publisher', $event.target.innerText)"
              >{{ book.publisher }}</dd>

              <dt class="col-sm-3">Created no earlier than</dt>
              <dd class="col-sm-9">
                <b-form-input
                  id="year-input-early"
                  type="date"
                  v-model="book.date_early"
                  @blur="edit_group('date_early', book.date_early)"
                />
              </dd>

              <dt class="col-sm-3">Created no later than</dt>
              <dd class="col-sm-9">
                <b-form-input
                  id="year-input-early"
                  type="date"
                  v-model="book.date_late"
                  @blur="edit_group('date_late', book.date_late)"
                />
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div class="col-6">
        <div class="card my-2">
          <div class="card-header">Components</div>
          <b-list-group flush>
            <b-list-group-item>
              <h5>spreads</h5>
              <p
                v-if="book.spreads.length>0"
                @click="detail_show='spreads'"
                class="clickable"
              >{{ book.spreads.length }} spreads</p>
              <p v-else>No spreads have been loaded for this book yet.</p>
            </b-list-group-item>
            <b-list-group-item v-for="(runs, runtype) in book.all_runs" :key="runtype">
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
                  >Delete</b-button>
                  <b-modal
                    :id="'delete-modal' + data.item.id"
                    :title="'Delete this ' + runtype + ' run?'"
                    ok-variant="danger"
                    ok-title="Delete"
                    @ok="run_delete(runtype, data.item.id)"
                  >This will wipe all data from the run, as well as any descendant book components. It cannot be undone.</b-modal>
                </template>
              </b-table>
              <p v-else>No runs for this segmentation type yet.</p>
            </b-list-group-item>
          </b-list-group>
        </div>
      </div>
    </div>
    <SpreadList v-if="detail_show=='spreads'" :spreads="book.spreads" />
    <PageList v-if="detail_show=='pages'" :page_run_id="selected_run_id" />
    <LineList
      v-if="detail_show=='lines'"
      :line_run_id="selected_run_id"
      :n_spreads="book.spreads.length"
    />
  </div>
</template>

<script>
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
    LineList
  },
  props: {
    id: String
  },
  data() {
    return {
      book: null,
      display_fields: ["date_started", "count", "erase"],
      detail_show: null,
      selected_run: null,
      selected_run_id: null
    };
  },
  methods: {
    run_delete: function(runtype, id) {
      console.log(runtype + " " + id);
      HTTP.delete("/runs/" + runtype + "/" + id + "/").then(
        results => {
          this.get_book(this.id);
          return results;
        },
        error => {
          console.log(error);
        }
      );
    },
    get_book: function(id) {
      return HTTP.get("/books/" + id + "/").then(
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
          date_started: this.display_date(r.date_started),
          count: r.component_count
        };
      });
    },
    select_run: function(payload) {
      const run_type = payload.type;
      const run_id = payload.id;
      if (run_type == "characters") {
        this.$router.push({
          name: "CharacterReviewView",
          query: { book: this.id, character_run: run_id }
        });
      } else if (run_type == "lines") {
        this.detail_show = run_type;
        this.selected_run_id = run_id;
      } else {
        return HTTP.get("/runs/" + run_type + "/" + run_id + "/").then(
          response => {
            this.selected_run = response.data;
            this.selected_run_id = run_id;
            this.detail_show = run_type;
          },
          error => {
            console.log(error);
          }
        );
      }
    },
    edit_group: function(fieldname, content) {
      var payload = {};
      payload[fieldname] = content;
      return HTTP.patch("/books/" + this.id + "/", payload).then(
        response => {
          this.$bvToast.toast(`${fieldname} updated`, {
            title: response.data.id,
            autoHideDelay: 5000,
            appendToast: true,
            variant: "success"
          });
        },
        error => {
          for (let [k, v] of Object.entries(error.response.data)) {
            this.$bvToast.toast(v, {
              title: error.response.status + ": " + k,
              autoHideDelay: 5000,
              appendToast: true,
              variant: "danger"
            });
          }
        }
      );
    }
  },
  created: function() {
    this.get_book(this.id);
  }
};
</script>

<style scoped>
.clickable {
  cursor: pointer;
}
</style>
