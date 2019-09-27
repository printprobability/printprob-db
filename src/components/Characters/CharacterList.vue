<template>
  <div id="charlist">
    <div class="card">
      <div class="card-header">Filter Characters</div>
      <div class="card-body" v-if="!freeze">
        <div class="row">
          <div class="col-4">
            <CharacterClassSelect
              :value="character_class"
              @input="$emit('character_class_input', $event)"
            />
          </div>
          <div class="col-4">
            <BookSelect :value="book" @input="$emit('book_input', $event)" />
          </div>
          <div class="col-4">
            <CharacterRunSelect
              :value="character_run"
              @input="$emit('character_run_input', $event)"
              :book="book"
            />
          </div>
        </div>
        <b-row>
          <div class="col-4">
            <BadCharacterRadio
              :value="bad_character"
              @input="$emit('bad_character_input', $event)"
            />
          </div>
          <div class="col-4">
            <CharacterOrderingSelect :value="order" @input="$emit('order_input', $event)" />
          </div>
        </b-row>
      </div>
      <div v-else class="card-body">
        <b-alert show variant="warning">{{ freeze_message }}</b-alert>
      </div>
    </div>
    <div class="char-images card my-2">
      <div class="card-header">
        <Spinner v-if="progress_spinner" />
        <div class="paginator" v-if="value.length>0 && !freeze">
          <p>Characters {{1 + (page - 1) * $APIConstants.REST_PAGE_SIZE }} to {{ (page - 1) * $APIConstants.REST_PAGE_SIZE + value.length }} out of {{ total_char_count }} characters</p>
          <b-pagination
            v-show="pagination_needed"
            :value="page"
            @input="$emit('page_input', $event)"
            :total-rows="total_char_count"
            :per-page="$APIConstants.REST_PAGE_SIZE"
            aria-controls="character-results"
          />
        </div>
        <div show v-else>No matching characters</div>
      </div>
      <div class="d-flex flex-wrap card-body" id="character-results" v-if="value.length>0">
        <CharacterImage
          v-for="character in value"
          :character="character"
          :key="character.id"
          :highlight="highlighted_characters.includes(character.id)"
          :bad="bad_characters.includes(character.id)"
          :good="good_characters.includes(character.id)"
          @char_clicked="$emit('char_clicked', $event)"
        />
      </div>
      <div class="card-footer" v-show="pagination_needed && !freeze">
        <b-pagination
          :value="page"
          @input="$emit('page_input', $event)"
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
    freeze: {
      type: Boolean,
      default: false
    },
    freeze_message: {
      type: String,
      default: ""
    },
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
    good_characters: {
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
    },
    value: {
      // Here is where the characters themselves live
      type: Array,
      default: () => []
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
      total_char_count: 0,
      bad_character: null,
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
    get_characters() {
      this.progress_spinner = true;
      return HTTP.get("/characters/", {
        params: {
          character_class: this.character_class,
          book: this.book,
          created_by_run: this.character_run,
          bad: this.bad_character,
          order: this.order,
          offset: this.rest_offset
        }
      }).then(
        response => {
          this.$emit("input", response.data.results);
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
    character_class() {
      this.get_characters();
    },
    book() {
      this.get_characters();
    },
    character_run() {
      this.get_characters();
    },
    order() {
      this.get_characters();
    },
    rest_offset() {
      this.get_characters();
    }
  },
  mounted() {
    this.get_characters();
  }
};
</script>

<style>
</style>
