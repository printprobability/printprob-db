<template>
  <b-form-select class="my-2" v-model="selected_book" :options="books" @input="select_book"></b-form-select>
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "BookSelect",
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
    },
    select_book: function() {
      this.$emit("selected", this.selected_book);
    }
  },
  created() {
    this.get_books();
  }
};
</script>