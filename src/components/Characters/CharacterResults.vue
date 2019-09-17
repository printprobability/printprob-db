<template>
  <div class="d-flex flex-wrap char-images">
    <CharacterImage v-for="character in characters" :character="character" :key="character.id" />
  </div>
</template>

<script>
import CharacterImage from "./CharacterImage";
import { HTTP } from "../../main";
export default {
  name: "CharacterResults",
  props: {
    selected_character_class: String,
    selected_book: null
  },
  components: {
    CharacterImage
  },
  data() {
    return {
      characters: [],
      total_char_count: null
    };
  },
  methods: {
    get_characters: function() {
      return HTTP.get("/characters/", {
        params: {
          character_class: this.selected_character_class,
          book: this.selected_book
        }
      }).then(
        response => {
          this.characters = response.data.results;
          this.total_char_count = response.data.count;
          this.prev_page = response.data.previous;
          this.next_page = response.data.next;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  watch: {
    selected_character_class: function() {
      this.get_characters();
    },
    selected_book: function() {
      this.get_characters();
    }
  }
};
</script>

<style>
</style>
