<template>
  <b-form-group id="book-group" label-for="book-select" label="Source book">
    <b-form-select
      id="book-select"
      class="my-2"
      :value="value"
      :options="books"
      @input="$emit('input', $event)"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "BookSelect",
  props: {
    value: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      books: []
    };
  },
  methods: {
    get_books: function() {
      return HTTP.get("/books/", { params: { images: true } }).then(
        response => {
          var book_options = _.concat(
            {
              text: "All books",
              value: null
            },
            response.data.results.map(x => {
              return { text: x.pq_title, value: x.id };
            })
          );
          this.books = book_options;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted() {
    this.get_books();
  }
};
</script>