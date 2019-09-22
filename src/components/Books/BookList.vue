<template>
  <div class="booklist">
    <div class="card my-2">
      <div class="card-header">Filter</div>
      <div class="card-body">
        <b-form-input v-model="publisher_search" placeholder="Search by partial publisher name" />
        <b-form-input v-model="title_search" placeholder="Search by partial title" />
      </div>
    </div>
    <div class="my-2">
      <BookResults :publisher="publisher_search" :title="title_search" />
    </div>
  </div>
</template>

<script>
import BookResults from "./BookResults";

export default {
  name: "BookList",
  components: {
    BookResults
  },
  data() {
    return {
      publisher_search: "",
      title_search: ""
    };
  }
};
</script>

<style>
</style>
