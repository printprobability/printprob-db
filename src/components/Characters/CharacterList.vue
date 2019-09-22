<template>
  <div id="charlist">
    <div class="card">
      <div class="card-header">Filter</div>
      <div class="card-body">
        <CharacterClassSelect
          :selected_character_class="selected_character_class"
          @selected="assign_selected_character"
        />
        <BookSelect @selected="assign_selected_book" />
      </div>
    </div>
    <CharacterResults
      :selected_character_class="selected_character_class"
      :selected_book="selected_book"
      :highlighted_characters="highlighted_characters"
      @update="update"
      @char_clicked="$emit('char_clicked', $event)"
    />
  </div>
</template>

<script>
import CharacterClassSelect from "../Menus/CharacterClassSelect";
import CharacterResults from "./CharacterResults";
import BookSelect from "../Menus/BookSelect";
import _ from "lodash";

export default {
  name: "CharacterList",
  props: {
    highlighted_characters: Array
  },
  components: {
    CharacterClassSelect,
    CharacterResults,
    BookSelect
  },
  data() {
    return {
      character_classes: [],
      selected_character_class: null,
      selected_book: null
    };
  },
  methods: {
    assign_selected_character: function(character_class) {
      this.selected_character_class = character_class;
    },
    assign_selected_book: function(book) {
      this.selected_book = book;
    },
    update: function(characters) {
      this.$emit("update", characters);
    }
  },
  watch: {
    selected_character_class: function() {
      this.$router.push({
        query: _.assign({}, this.$route.query, {
          character_class: this.selected_character_class
        })
      });
    },
    selected_book: function() {
      this.$router.push({
        query: _.assign({}, this.$route.query, {
          book: this.selected_book
        })
      });
    }
  },
  mounted: function() {
    this.selected_character_class = this.$route.query.character_class;
    this.selected_book = this.$route.query.book;
  }
};
</script>

<style>
</style>
