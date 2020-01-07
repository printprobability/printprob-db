<template>
  <b-container class="my-2">
    <b-card header="Create a new book">
      <b-form-row>
        <b-col col md="4">
          <b-form-group id="eebo-group" label="EEBO id" label-for="eebo-input">
            <b-form-input
              id="eebo-input"
              v-model="eebo"
              placeholder="99896497"
              type="number"
              no-wheel
            />
          </b-form-group>
          <b-form-group id="vid-group" label="VID" label-for="vid-input">
            <b-form-input id="vid-input" v-model="vid" placeholder="184449" type="number" no-wheel />
          </b-form-group>
          <b-form-group id="tcp-group" label="tcp" label-for="tcp-input">
            <b-form-input id="tcp-input" v-model="tcp" placeholder="A27900" />
          </b-form-group>
          <b-form-group id="estc-group" label="estc" label-for="estc-input">
            <b-form-input id="estc-input" v-model="estc" placeholder="R23698" />
          </b-form-group>
        </b-col>
        <b-col col md="4">
          <b-form-group id="title-group" label-for="title-input" label="Title">
            <b-form-input id="title-input" v-model="title" placeholder="nine arguments" required />
          </b-form-group>
          <b-form-group id="publisher-group" label="Publisher" label-for="publisher-input">
            <b-form-input id="publisher-input" v-model="publisher" placeholder="overton" />
          </b-form-group>
          <b-form-group id="author-group" label-for="author-input" label="author">
            <b-form-input id="author-input" v-model="author" placeholder="milton" />
          </b-form-group>
        </b-col>
        <b-col col md="4">
          <b-form-group id="date-range-group" label="Published between" description>
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
      eebo: null,
      vid: null,
      tcp: "",
      estc: "",
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
        eebo: this.eebo,
        vid: this.vid,
        tcp: this.tcp,
        estc: this.estc,
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
          this.$router.push({
            name: "BookDetailView",
            params: { id: response.data.id }
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