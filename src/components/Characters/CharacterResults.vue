<template>
  <div class="char-images card my-2">
    <div class="card-header">
      <Spinner v-if="progress_spinner" />
      <div class="paginator" v-if="characters.length>0">
        <p>Characters {{1 + (page - 1) * $APIConstants.REST_PAGE_SIZE }} to {{ (page - 1) * $APIConstants.REST_PAGE_SIZE + characters.length }} out of {{ total_char_count }} characters</p>
        <b-pagination
          v-show="pagination_needed"
          v-model="page"
          :total-rows="total_char_count"
          :per-page="$APIConstants.REST_PAGE_SIZE"
          aria-controls="character-results"
        />
      </div>
      <div v-else>No matching characters</div>
    </div>
    <div class="d-flex flex-wrap card-body" id="character-results" v-if="characters.length>0">
      <CharacterImage
        v-for="character in characters"
        :character="character"
        :key="character.id"
        :highlight="highlighted_characters.includes(character.id)"
        @char_clicked="$emit('char_clicked', $event)"
      />
    </div>
    <div class="card-footer" v-show="pagination_needed">
      <b-pagination
        v-model="page"
        :total-rows="total_char_count"
        :per-page="$APIConstants.REST_PAGE_SIZE"
        aria-controls="character-results"
      />
    </div>
  </div>
</template>

<script>
import CharacterImage from "./CharacterImage";
import Spinner from "../Interfaces/Spinner";
import { HTTP, APIConstants } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterResults",
  props: {
    selected_character_class: String,
    selected_book: null,
    highlighted_characters: Array
  },
  components: {
    CharacterImage,
    Spinner
  },
  data() {
    return {
      characters: [],
      total_char_count: 0,
      page: 1,
      progress_spinner: false
    };
  },
  computed: {
    pagination_needed: function() {
      return this.total_char_count > this.$APIConstants.REST_PAGE_SIZE;
    },
    rest_offset: function() {
      return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    }
  },
  methods: {
    get_characters: function() {
      this.progress_spinner = true;
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
          this.progress_spinner = false;
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
      window.scrollTo(0, 0);
      this.get_characters();
    },
    page: function() {
      this.$router.push({
        query: _.assign({}, this.$route.query, {
          page: this.page
        })
      });
    },
    characters: function() {
      this.$emit("update", this.characters);
    }
  },
  mounted: function() {
    if (!!this.$route.query.page) {
      this.page = this.$route.query.page;
    }
  }
};
</script>

<style>
</style>
