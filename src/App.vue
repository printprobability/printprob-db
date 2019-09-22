<template>
  <div class="container">
    <b-navbar toggleable="lg" type="dark" variant="secondary">
      <b-navbar-brand to="/">Print & Probability</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/books">View Books</b-nav-item>
          <b-nav-item to="/group_characters">Edit Groupings</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view></router-view>
    <nav class="navbar sticky-bottom navbar-dark bg-secondary">
      <b-nav-text>
        ©
        <a href="https://library.cmu.edu">Carnegie Mellon University Libraries</a> 2019. Built by
        <a href="https://matthewlincoln.net">Matthew Lincoln</a>.
      </b-nav-text>
    </nav>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {},
  methods: {},
  mounted: function() {}
};
</script>

<style>
</style>
