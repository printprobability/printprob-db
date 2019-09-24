<template>
  <b-jumbotron header="Print & Probability Workbench" class="m-5">
    <template v-slot:lead>
      An interactive viewer and editor for Carnegie Mellon University's
      <em>Print and Probability</em> project to create a dictionary of distinctive early modern type.
    </template>
    <hr class="my-4" />
    <b-button v-if="!logged_in" :href="$APIConstants.API_LOGIN" variant="primary">Log In</b-button>
    <template v-else>
      <p>{{ display_count }}</p>
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
      nchars: null
    };
  },
  computed: {
    display_count: function() {
      if (!!this.nchars) {
        return (
          "Indexing " +
          this.nchars.toLocaleString() +
          " characters and counting..."
        );
      } else {
        return "???";
      }
    }
  },
  methods: {
    get_nchars: function() {
      return HTTP.get("/characters/", {
        params: {
          limit: 1
        }
      }).then(
        response => {
          this.nchars = response.data.count;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_nchars();
  }
};
</script>