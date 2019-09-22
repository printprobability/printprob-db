<template>
  <b-jumbotron header="Print Viewer" :lead="display_count" class="my-2">
    <p>
      An interactive viewer and editor for Carnegie Mellon University's
      <em>Print and Probability</em> project to create a dictionary of distinctive early modern type.
    </p>
    <b-button variant="primary" href="http://localhost/api-authlogin">Log in</b-button>
  </b-jumbotron>
</template>

<script>
import { HTTP } from "../main";
export default {
  name: "Home",
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
        return "";
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