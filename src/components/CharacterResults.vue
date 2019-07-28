<template>
  <div class="d-flex flex-wrap char-images">
    <CharacterImage v-for="character in characters" :character="character" :key="character.id" />
  </div>
</template>

<script>
import CharacterImage from "./CharacterImage.vue";
export default {
  name: "CharacterResults",
  props: {
    selected_character_class: String
  },
  components: {
    CharacterImage
  },
  data: function(d) {
    return {
      characters: [],
      total_char_count: Number,
      prev_page: String,
      next_page: String
    };
  },
  methods: {
    get_characters: function() {
      console.log(this.selected_character_class);
      return this.$http
        .get("http://localhost/characters/", {
          params: { character_class: this.selected_character_class }
        })
        .then(
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
  mounted: function() {
    this.get_characters();
  }
};
</script>

<style>
</style>
