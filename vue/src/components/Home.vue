<template>
  <b-jumbotron header="Print & Probability Workbench" class="m-5">
    <template v-slot:lead>
      An interactive viewer and editor for Carnegie Mellon University's
      <em>Print and Probability</em> project to create a dictionary of distinctive early modern type.
    </template>
    <hr class="my-4" />
    <b-button v-if="!logged_in" :href="$APIConstants.API_LOGIN" variant="primary">Log In</b-button>
  </b-jumbotron>
</template>

<script>
export default {
  name: "Home",
  props: {
    logged_in: Boolean
  },
  data() {
    return {};
  }
};
</script>