<template>
  <div class="booklist">
    <div class="card my-2">
      <div class="card-header">Filter books</div>
      <div class="card-body">
        <b-form-group
          id="publisher-group"
          label="Publisher"
          label-for="publisher-input"
          description="Partial publisher name (case insensitive)"
        >
          <b-form-input id="publisher-input" v-model="publisher_search" placeholder="overton" />
        </b-form-group>
        <b-form-group
          id="title-group"
          label-for="title-input"
          label="Title"
          description="Search by partial title (case insensitive)"
        >
          <b-form-input id="title-input" v-model="title_search" placeholder="nine arguments" />
        </b-form-group>
      </div>
    </div>
    <BookResults :publisher="publisher_search" :title="title_search" />
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
