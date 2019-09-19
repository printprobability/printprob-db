<template>
  <div class="char-images">
    <div class="paginator">
      <p>Displaying {{ characters.length }} out of {{ total_char_count }} characters</p>
      <b-pagination
        v-show="pagination_needed"
        v-model="page"
        :total-rows="total_char_count"
        :per-page="REST_PAGE_SIZE"
        aria-controls="character-results"
      />
    </div>
    <div class="d-flex flex-wrap" id="character-results">
      <CharacterImage v-for="character in characters" :character="character" :key="character.id" />
    </div>
  </div>
</template>

<script>
import CharacterImage from "./CharacterImage";
import { HTTP, APIConstants } from "../../main";

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
      total_char_count: 0,
      page: 1,
      REST_PAGE_SIZE: APIConstants.REST_PAGE_SIZE
    };
  },
  computed: {
    pagination_needed: function() {
      return this.total_char_count > this.REST_PAGE_SIZE;
    },
    rest_offset: function() {
      return (this.page - 1) * this.REST_PAGE_SIZE;
    }
  },
  methods: {
    get_characters: function() {
      return HTTP.get("/characters/", {
        params: {
          character_class: this.selected_character_class,
          book: this.selected_book,
          offset: this.rest_offset
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
    },
    rest_offset: function() {
      this.get_characters();
    },
    characters: function() {
      this.$emit("update", this.characters);
    }
  }
};
</script>

<style>
</style>
