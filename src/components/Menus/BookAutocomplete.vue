<template>
  <div>
    <b-form-group
      id="book-autocomplete-group"
      label-for="book-autocomplete-select"
      label="Source book"
      description="Begin typing for suggestions"
    >
      <b-input-group>
        <template v-slot:append v-if="!!query">
          <b-input-group-text class="input-clear" @click="clear_input">x</b-input-group-text>
        </template>
        <b-form-input
          id="book-autocomplete-select"
          v-model="query"
          placeholder="an answer to nine"
          @input="start_query"
        />
      </b-input-group>
      <div v-show="show_dropdown" class="results-dropdown">
        <b-list-group>
          <b-list-group-item v-if="progress_spinner">
            <Spinner />
          </b-list-group-item>
          <b-list-group-item
            button
            v-for="book in books"
            :key="book.id"
            @click="select_book(book)"
          >{{ book.text }}</b-list-group-item>
        </b-list-group>
      </div>
    </b-form-group>
  </div>
</template>

<script>
import { HTTP } from "../../main";
import Spinner from "../Interfaces/Spinner";
import _ from "lodash";

export default {
  name: "BookAutocomplete",
  components: {
    Spinner
  },
  props: {
    value: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      query: "",
      books: [],
      selected_book: null,
      progress_spinner: false
    };
  },
  computed: {
    show_dropdown() {
      return !this.selected_book && !!this.query;
    }
  },
  methods: {
    start_query(val) {
      this.progress_spinner = true;
      this.get_books(val);
    },
    get_books: _.debounce(function(val) {
      if (!val) {
        this.books = [];
        return null;
      } else if (!val.length > 0) {
        this.books = [];
        return null;
      }
      this.selected_book = null;
      return HTTP.get("/books/", {
        params: { pq_title: val, images: true, limit: 10 }
      }).then(
        response => {
          if (response.data.count > 0) {
            this.books = response.data.results.map(x => {
              return { text: x.label, value: x.id };
            });
          } else {
            this.books = [{ text: "No matching books", value: null }];
          }
          this.progress_spinner = false;
        },
        error => {
          console.log(error);
          this.progress_spinner = false;
        }
      );
    }, 300),
    select_book(book) {
      this.$emit("input", book.value);
      this.query = book.text;
      this.selected_book = book.value;
      this.books = [];
    },
    clear_input() {
      this.$emit("input", null);
      this.query = null;
    }
  },
  watch: {
    query() {
      if (!this.query) {
        this.$emit("input", null);
      } else {
        if (this.query.length <= 0) {
          this.$emit("input", null);
        }
      }
    }
  },
  created() {
    this.selected_book = this.value;
    this.query = this.value;
  }
};
</script>

<style scoped>
.results-dropdown {
  position: absolute;
  display: inline-block;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.input-clear {
  cursor: pointer;
}
</style>