<template>
  <b-container class="my-2">
    <b-card header="Create a new book">
      <b-form-row>
        <b-col col md="4">
          <b-form-group
            id="vid-group"
            label="VID"
            label-for="vid-input"
            description="Enter a VID for a known book from EEBO to prepopulate these fields."
          >
            <b-form-input
              id="vid-input"
              v-model="vid"
              placeholder="184449"
              type="number"
              no-wheel
              debounce="750"
            />
          </b-form-group>
          <b-form-group id="eebo-group" label="EEBO id" label-for="eebo-input">
            <b-form-input
              id="eebo-input"
              v-model="eebo"
              placeholder="99896497"
              type="number"
              no-wheel
            />
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
            <b-form-input
              id="title-input"
              v-model="title"
              placeholder="nine arguments"
              required
              :state="title != ''"
            />
          </b-form-group>
          <b-form-group
            id="publisher-group"
            label="Publisher"
            label-for="publisher-input"
          >
            <b-form-input
              id="publisher-input"
              v-model="publisher"
              placeholder="overton"
            />
          </b-form-group>
          <b-form-group
            id="author-group"
            label-for="author-input"
            label="Author"
          >
            <b-form-input
              id="author-input"
              v-model="author"
              placeholder="milton"
            />
          </b-form-group>
          <b-form-group
            id="repository-group"
            label-for="repository-input"
            label="Repository"
          >
            <b-form-input
              id="repository-input"
              v-model="repository"
              placeholder="British Library"
            />
          </b-form-group>
        </b-col>
        <b-col col md="4">
          <b-form-group
            id="date-range-group"
            label="Published between"
            description
          >
            <b-form inline>
              <b-form-input
                class="mx-2"
                id="year-input-early"
                type="date"
                v-model="date_early"
                :state="date_early != ''"
                required
              />and
              <b-form-input
                class="mx-2"
                id="year-input-late"
                type="date"
                v-model="date_late"
                :state="date_late != ''"
                required
              />
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
import moment from "moment";
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
      repository: "",
      date_early: "",
      date_late: "",
    };
  },
  methods: {
    cancel() {
      this.$router.push({ name: "BookListView" });
    },
    date_to_number(d) {
      return Number(moment(new Date(d)).format("YYYY"));
    },
    populate_from_vid(vid) {
      if (!!vid) {
        HTTP.get("/books/", { params: { vid: vid } }).then(
          (response) => {
            if (response.data.count >= 1) {
              const retrieved_book = response.data.results[0];
              this.$bvToast.toast(`Data retrieved`, {
                title: retrieved_book.pq_title,
                autoHideDelay: 5000,
                appendToast: true,
                variant: "success",
              });
              this.eebo = retrieved_book.eebo;
              this.tcp = retrieved_book.tcp;
              this.estc = retrieved_book.estc;
              this.title = retrieved_book.pq_title;
              this.publisher = retrieved_book.pq_publisher;
              this.author = retrieved_book.pq_author;
              this.author = retrieved_book.repository;
              this.date_early = `${retrieved_book.pq_year_early}-01-01`;
              this.date_late = `${retrieved_book.pq_year_late}-12-31`;
            } else {
              this.$bvToast.toast(`Failed`, {
                title: `No book with VID ${vid}`,
                autoHideDelay: 5000,
                appendToast: true,
                variant: "warning",
              });
            }
          },
          (error) => {
            this.$bvToast.toast(error, {
              title: "Error",
              autoHideDelay: 5000,
              appendToast: true,
              variant: "danger",
            });
          }
        );
      }
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
        repository: this.repository,
        pq_year_early: this.date_to_number(this.date_early),
        pq_year_late: this.date_to_number(this.date_late),
        date_early: this.date_early,
        date_late: this.date_late,
      };
      HTTP.post("/books/", payload).then(
        (response) => {
          this.$bvToast.toast(`Book created`, {
            title: response.data.pq_title,
            autoHideDelay: 5000,
            appendToast: true,
            variant: "success",
          });
          this.$router.push({
            name: "BookDetailView",
            params: { id: response.data.id },
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
  },
  watch: {
    vid() {
      this.populate_from_vid(this.vid);
    },
  },
};
</script>