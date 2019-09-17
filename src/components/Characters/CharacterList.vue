<template>
  <div id="charlist">
    <div class="card m-2">
      <CharacterClassSelect @selected="assign_selected_character" />
      <BookSelect @selected="assign_selected_book" />
    </div>
    <CharacterResults
      :selected_character_class="selected_character_class"
      :selected_book="selected_book"
    />
  </div>
</template>

<script>
import CharacterClassSelect from "../Menus/CharacterClassSelect";
import CharacterResults from "./CharacterResults";
import BookSelect from "../Menus/BookSelect";

export default {
  name: "CharacterList",
  components: {
    CharacterClassSelect,
    CharacterResults,
    BookSelect
  },
  data() {
    return {
      character_classes: [],
      selected_character_class: "",
      selected_book: null
    };
  },
  methods: {
    assign_selected_character: function(character_class) {
      this.selected_character_class = character_class;
    },
    assign_selected_book: function(book) {
      this.selected_book = book;
    }
  }
};
</script>

<style>
</style>
