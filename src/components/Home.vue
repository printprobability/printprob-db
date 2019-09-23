<template>
  <b-jumbotron header="Print & Probability Viewer" class="my-2">
    <p>
      An interactive viewer and editor for Carnegie Mellon University's
      <em>Print and Probability</em> project to create a dictionary of distinctive early modern type.
    </p>
    <b-button v-if="!logged_in" :href="$APIConstants.API_LOGIN" variant="primary">Log In</b-button>
    <template v-else>
      <h4>{{ display_count }}</h4>
      <p>
        <b-button to="/books" variant="info">Browse books</b-button>
      </p>
      <p>
        <b-button to="/group_characters" variant="info">Edit character groups</b-button>
      </p>
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