<template>
  <b-jumbotron header="Print & Probability Workbench" class="m-5">
    <template v-slot:lead>
      An interactive viewer and editor for Carnegie Mellon University's
      <em>Print and Probability</em> project to create a dictionary of distinctive early modern type.
    </template>
    <hr class="my-4" />
    <b-button v-if="!logged_in" :href="$APIConstants.API_LOGIN" variant="primary">Log In</b-button>
    <template v-else>
      <p v-show="!!display_count">{{ display_count }}</p>
    </template>
  </b-jumbotron>
</template>

<script>
import { HTTP } from "../main";
export default {
  name: "Home",
  props: {
    logged_in: Boolean
  },
  data() {
    return {
      nchars: null,
      nbooks: null
    };
  },
  computed: {
    display_count: function() {
      if (!!this.nchars && !!this.nbooks) {
        return (
          "Indexing " +
          this.nbooks.toLocaleString() +
          " books with about " +
          this.nchars.toLocaleString() +
          " characters and counting..."
        );
      } else {
        return null;
      }
    }
  },
  methods: {
    get_nchars: function() {
      return HTTP.get("/lines/count/").then(
        response => {
          this.nchars = response.data.count * 80;
        },
        error => {
          console.log(error);
        }
      );
    },
    get_nbooks: function() {
      return HTTP.get("/books/count/").then(
        response => {
          this.nbooks = response.data.count;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_nchars();
    this.get_nbooks();
  }
};
</script>