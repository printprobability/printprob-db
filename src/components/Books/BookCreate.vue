<template>
  <b-container class="my-2">
    <b-card header="Create a new book">
      <b-form-row>
        <b-col col md="6">
          <b-form-group id="title-group" label-for="title-input" label="Title">
            <b-form-input id="title-input" v-model="title" placeholder="nine arguments" />
          </b-form-group>
          <b-form-group id="publisher-group" label="Publisher" label-for="publisher-input">
            <b-form-input id="publisher-input" v-model="publisher" placeholder="overton" />
          </b-form-group>
          <b-form-group id="author-group" label-for="author-input" label="author">
            <b-form-input id="author-input" v-model="author" placeholder="milton" />
          </b-form-group>
        </b-col>
        <b-col col md="6">
          <b-form-group
            id="date-range-group"
            label="Books published between"
            description="Only books whose dates overlap the specified range"
          >
            <b-form inline>
              <b-form-input class="mx-2" id="year-input-early" type="date" v-model="date_early" />and
              <b-form-input class="mx-2" id="year-input-late" type="date" v-model="date_late" />
            </b-form>
          </b-form-group>
        </b-col>
      </b-form-row>
      <template v-slot:footer>
        <div class="d-flex justify-content-between">
          <b-button variant="warning" @click="cancel">Cancel</b-button>
          <b-button variant="success" @click="submit">Create</b-button>
        </div>
      </template>
    </b-card>
  </b-container>
</template>

<script>
import { HTTP } from "../../main";
export default {
  name: "BookCreate",
  data() {
    return {
      title: "",
      publisher: "",
      author: "",
      date_early: "",
      date_late: ""
    };
  },
  methods: {
    cancel() {
      this.$router.push({ name: "BookListView" });
    },
    submit() {
      const payload = {
        pq_title: this.title,
        pp_publisher: this.publisher,
        pp_author: this.author,
        pp_date_early: this.date_early,
        pp_date_late: this.date_late
      };
      HTTP.post("/books/", payload).then(
        response => {
          this.$bvToast.toast(`Book created`, {
            title: response.data.pq_title,
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
  }
};
</script>