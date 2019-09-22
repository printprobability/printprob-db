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
