<template>
  <b-container fluid class="p-0 d-flex flex-column parent">
    <b-navbar toggleable="lg" type="dark" variant="secondary">
      <b-navbar-brand to="/">Print & Probability</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-if="logged_in">
          <b-nav-item to="/books">Browse Books</b-nav-item>
          <b-nav-dropdown text="Tasks">
            <b-dropdown-item to="/character_review"
              >Review Characters</b-dropdown-item
            >
            <b-dropdown-item to="/group_characters"
              >Edit Groupings</b-dropdown-item
            >
          </b-nav-dropdown>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-dropdown text="API">
            <b-dropdown-item href="/api/">Browsable API</b-dropdown-item>
            <b-dropdown-item href="/api/docs">Documentation</b-dropdown-item>
          </b-nav-dropdown>
          <b-nav-item v-if="logged_in" :href="$APIConstants.API_LOGOUT"
            >Logout</b-nav-item
          >
          <b-nav-item v-else :href="$APIConstants.API_LOGIN">Login</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view :logged_in="logged_in"></router-view>
    <nav class="navbar sticky-bottom navbar-dark bg-secondary">
      <b-navbar-nav>
        <b-nav-text>
          ©
          <a href="https://library.cmu.edu"
            >Carnegie Mellon University Libraries</a
          >
          2021. Built by
          <a href="https://matthewlincoln.net">Matthew Lincoln</a>.
        </b-nav-text>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item href="https://github.com/cmu-lib/printprob-db"
          >GitHub</b-nav-item
        >
      </b-navbar-nav>
    </nav>
  </b-container>
</template>

<script>
import { HTTP } from './main'
export default {
  name: 'app',
  data() {
    return {
      logged_in: false,
    }
  },
  methods: {},
  mounted: function () {
    return HTTP.get('/', {}).then(
      (response) => {
        this.logged_in = !!response
      },
      (error) => {
        console.log(error)
        this.logged_in = false
      }
    )
  },
}
</script>

<style>
.parent {
  min-height: 100vh;
}
</style>
