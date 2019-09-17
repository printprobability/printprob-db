<template>
  <div class="booklist">
    <h1>Search Books</h1>
    <div class="card m-2">
      <div class="card-header">Options</div>
      <div class="card-body">
        <b-form-input v-model="publisher_name_search" placeholder="Enter partial publisher name" />
      </div>
    </div>
    <div class="card m-2">
      <BookResults :publisher="debounced_publisher_name" />
    </div>
  </div>
</template>

<script>
import BookResults from "./BookResults";
import _ from "lodash";
import { APIConstants } from "../../main";

export default {
  name: "BookList",
  components: {
    BookResults
  },
  data() {
    return {
      publisher_name_search: "",
      debounced_publisher_name: ""
    };
  },
  watch: {
    publisher_name_search: _.debounce(function() {
      this.debounced_publisher_name = this.publisher_name_search;
    }, APIConstants.DEBOUNCE_DELAY)
  }
};
</script>

<style>
</style>
