<template>
  <b-form-group id="book-group" label-for="book-select" label="Source book">
    <b-form-select
      id="book-select"
      class="my-2"
      v-model="selected_book"
      :options="books"
      @input="$emit('input', selected_book)"
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
      selected_book: null,
      books: []
    };
  },
  methods: {
    get_books: function() {
      return HTTP.get("/books/").then(
        response => {
          var book_options = _.concat(
            {
              text: "Select books",
              value: null
            },
            response.data.results.map(x => {
              return { text: x.publisher + " - " + x.title, value: x.eebo };
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
  created() {
    this.get_books();
    this.selected_book = this.value;
  }
};
</script>