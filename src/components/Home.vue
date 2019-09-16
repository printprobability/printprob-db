<template>
  <b-jumbotron header="Print Viewer" lead>
    <p>
      An interactive viewer for Carnegie Mellon University's
      <em>Print and Probability</em> project to create a dictionary of distinctive early modern type.
    </p>
    <b-button variant="primary" href="/api-authlogin/?next=localhost:8080/books">Log in</b-button>
  </b-jumbotron>
</template>

<script>
export default {
  name: "PageImage"
};
</script>