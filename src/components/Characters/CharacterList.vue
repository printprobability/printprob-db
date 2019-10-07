<template>
  <div id="charlist">
    <div class="card">
      <div class="card-header">Filter Characters</div>
      <div class="card-body">
        <div class="row">
          <div class="col-4">
            <CharacterClassSelect
              :value="character_class"
              @input="$emit('character_class_input', $event)"
            />
          </div>
          <div class="col-4">
            <BookAutocomplete :value="book" @input="$emit('book_input', $event)" />
          </div>
          <div class="col-4">
            <CharacterRunSelect
              v-if="!!book"
              :value="character_run"
              @input="$emit('character_run_input', $event)"
              :book="book"
            />
          </div>
        </div>
        <b-row>
          <div class="col-4">
            <CharacterAgreementRadio
              :value="char_agreement"
              @input="$emit('char_agreement_input', $event)"
            />
          </div>
          <div class="col-4">
            <CharacterOrderingSelect :value="order" @input="$emit('order_input', $event)" />
          </div>
        </b-row>
      </div>
    </div>
    <div class="char-images card my-2">
      <div class="card-header">
        <Spinner v-if="progress_spinner" />
        <div class="paginator" v-if="value.length>0">
          <CursorButtons :prev="prev" :next="next" @cursor="page_cursor($event)" />
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
    </div>
  </div>
</template>

<script>
import CharacterClassSelect from "../Menus/CharacterClassSelect";
import CharacterOrderingSelect from "../Menus/CharacterOrderingSelect";
import BookAutocomplete from "../Menus/BookAutocomplete";
import CharacterAgreementRadio from "../Menus/CharacterAgreementRadio";
import CharacterRunSelect from "../Menus/CharacterRunSelect";
import CharacterImage from "./CharacterImage";
import Spinner from "../Interfaces/Spinner";
import CursorButtons from "../Menus/CursorButtons";
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
      type: String
    },
    order: {
      default: "-class_probability",
      type: String
    },
    char_agreement: {
      default: "all",
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
    BookAutocomplete,
    CharacterAgreementRadio,
    CharacterImage,
    Spinner,
    CursorButtons
  },
  data() {
    return {
      total_char_count: 0,
      progress_spinner: false,
      next: null,
      prev: null,
      cursor: null
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
    cursor_param(url) {
      if (!!url) {
        const cursor_match = url.match(/cursor=([^&]+)/);
        if (!!cursor_match) {
          return decodeURIComponent(cursor_match[1]);
        }
      } else {
        return null;
      }
    },
    page_cursor(cursor) {
      this.cursor = cursor;
      this.get_characters();
    },
    get_characters() {
      this.progress_spinner = true;
      return HTTP.get("/characters/", {
        params: {
          character_class: this.character_class,
          book: this.book,
          created_by_run: this.character_run,
          agreement: this.char_agreement,
          order: this.order,
          cursor: this.cursor
        }
      }).then(
        response => {
          this.$emit("input", response.data.results);
          this.cursor = null;
          this.prev = this.cursor_param(response.data.previous);
          this.next = this.cursor_param(response.data.next);
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
    char_agreement() {
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
