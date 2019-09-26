<template>
  <div id="charlist">
    <div class="card">
      <div class="card-header">Filter Characters</div>
      <div class="card-body">
        <div class="row">
          <div class="col-4">
            <CharacterClassSelect v-model="selected_character_class" />
          </div>
          <div class="col-4">
            <BookSelect v-model="selected_book" />
          </div>
          <div class="col-4">
            <CharacterRunSelect v-model="selected_character_run" :book="selected_book" />
          </div>
        </div>
        <b-row>
          <div class="col-4">
            <BadCharacterRadio v-model="bad_character" />
          </div>
          <div class="col-4">
            <CharacterOrderingSelect v-model="selected_order" />
          </div>
        </b-row>
      </div>
    </div>
    <div class="char-images card my-2">
      <div class="card-header">
        <Spinner v-if="progress_spinner" />
        <div class="paginator" v-if="characters.length>0">
          <p>Characters {{1 + (selected_page - 1) * $APIConstants.REST_PAGE_SIZE }} to {{ (selected_page - 1) * $APIConstants.REST_PAGE_SIZE + characters.length }} out of {{ total_char_count }} characters</p>
          <b-pagination
            v-show="pagination_needed"
            v-model="selected_page"
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
          :bad="bad_characters.includes(character.id)"
          @char_clicked="$emit('char_clicked', $event)"
        />
      </div>
      <div class="card-footer" v-show="pagination_needed">
        <b-pagination
          v-model="selected_page"
          :total-rows="total_char_count"
          :per-page="$APIConstants.REST_PAGE_SIZE"
          aria-controls="character-results"
        />
      </div>
    </div>
  </div>
</template>

<script>
import CharacterClassSelect from "../Menus/CharacterClassSelect";
import CharacterOrderingSelect from "../Menus/CharacterOrderingSelect";
import BookSelect from "../Menus/BookSelect";
import BadCharacterRadio from "../Menus/BadCharacterRadio";
import CharacterRunSelect from "../Menus/CharacterRunSelect";
import CharacterImage from "./CharacterImage";
import Spinner from "../Interfaces/Spinner";
import { HTTP } from "../../main";

export default {
  name: "CharacterList",
  props: {
    highlighted_characters: {
      type: Array,
      default: function() {
        return [];
      }
    },
    bad_characters: {
      type: Array,
      default: function() {
        return [];
      }
    },
    page: {
      default: 1,
      type: Number
    },
    character_class: {
      default: null,
      type: String
    },
    book: {
      default: null,
      type: Number
    },
    order: {
      default: "-class_probability",
      type: String
    },
    character_run: {
      default: null,
      type: String
    }
  },
  components: {
    CharacterClassSelect,
    CharacterOrderingSelect,
    CharacterRunSelect,
    BookSelect,
    BadCharacterRadio,
    CharacterImage,
    Spinner
  },
  data() {
    return {
      characters: [],
      character_classes: [],
      total_char_count: 0,
      bad_character: null,
      progress_spinner: false,
      selected_page: this.page,
      selected_character_class: this.character_class,
      selected_character_run: this.character_run,
      selected_book: this.book,
      selected_order: this.order
    };
  },
  computed: {
    pagination_needed: function() {
      return this.total_char_count > this.$APIConstants.REST_PAGE_SIZE;
    },
    rest_offset: function() {
      return (this.selected_page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    }
  },
  methods: {
    get_characters: function() {
      this.progress_spinner = true;
      return HTTP.get("/characters/", {
        params: {
          character_class: this.selected_character_class,
          book: this.selected_book,
          created_by_run: this.selected_character_run,
          bad: this.bad_character,
          order: this.selected_order,
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
          this.progress_spinner = false;
        }
      );
    }
  },
  watch: {
    characters: function() {
      this.$emit("update", this.characters);
    },
    selected_character_class: function() {
      this.get_characters();
    },
    selected_character_run: function() {
      this.get_characters();
    },
    selected_book: function() {
      this.get_characters();
    },
    selected_page: function() {
      this.get_characters();
    },
    bad_character: function() {
      this.get_characters();
    },
    selected_order: function() {
      this.get_characters();
    }
  },
  created() {
    this.get_characters();
  }
};
</script>

<style>
</style>
