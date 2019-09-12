<template>
  <div id="app">
    <b-form-select
      v-model="selected_character_class"
      :options="character_classes"
      @input="input_swap"
    ></b-form-select>
    <b-form-select v-model="selected_book" :options="book_ids" @input="input_swap"></b-form-select>
    <CharacterResults
      :selected_character_class="this.$route.query.classname"
      :selected_book="this.$route.query.book"
      :key="this.$route.query.classname + this.$route.query.book"
    />
  </div>
</template>

<script>
import CharacterResults from "./CharacterResults.vue";

export default {
  name: "CharacterList",
  components: {
    CharacterResults
  },
  data: function(d) {
    return {
      character_classes: [],
      book_ids: [],
      selected_character_class: String,
      selected_book: Number
    };
  },
  methods: {
    input_swap: function() {
      this.$router.push({
        name: "CharacterListView",
        query: {
          classname: this.selected_character_class,
          book: this.selected_book
        }
      });
    },
    get_charcacter_classes: function() {
      return this.$http.get("http://localhost/character_classes/").then(
        response => {
          this.character_classes = response.data.results.map(x => x.classname);
        },
        error => {
          console.log(error);
        }
      );
    },
    get_book_ids: function() {
      return this.$http.get("http://localhost/books/").then(
        response => {
          this.book_ids = response.data.results.map(x => x.eebo);
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_charcacter_classes();
    this.get_book_ids();
    this.selected_character_class = this.$route.query.classname;
    this.selected_book = this.$route.query.book;
  }
};
</script>

<style>
</style>
