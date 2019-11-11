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
          <p>
            Characters {{1 + (page - 1) * $APIConstants.REST_PAGE_SIZE }} to {{ (page - 1) * $APIConstants.REST_PAGE_SIZE + value.length }}
            <span
              v-if="this.results.next"
              v-b-tooltip.hover
              title="Arbitrarily counting characters is a very expensive operation, so we only estimate here..."
            >(out of many)</span>
          </p>
          <b-pagination
            hide-goto-end-buttons
            v-show="pagination_needed"
            :value="page"
            @input="$emit('page_input', $event)"
            :per-page="$APIConstants.REST_PAGE_SIZE"
            :total-rows="mock_rows"
            aria-controls="character-results"
            limit="3"
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
    Spinner
  },
  data() {
    return {
      progress_spinner: false,
      cursor: null
    };
  },
  asyncComputed: {
    results() {
      this.progress_spinner = true;
      return HTTP.get("/characters/", {
        params: {
          limit: this.$APIConstants.REST_PAGE_SIZE,
          offset: this.rest_offset,
          character_class: this.character_class,
          book: this.book,
          created_by_run: this.character_run,
          agreement: this.char_agreement,
          ordering: this.order,
          cursor: this.cursor
        }
      }).then(
        response => {
          this.progress_spinner = false;
          return response.data;
        },
        error => {
          this.progress_spinner = false;
          console.log(error);
        }
      );
    }
  },
  computed: {
    rest_offset: function() {
      return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    },
    pagination_needed: function() {
      return !!this.results.next || !!this.results.previous;
    },
    mock_rows: function() {
      var baseline = this.rest_offset + this.value.length;
      if (!!this.results.next) {
        baseline += this.$APIConstants.REST_PAGE_SIZE;
      }
      return baseline;
    }
  },
  watch: {
    results() {
      this.$emit("input", this.results.results);
    },
    book() {
      if (!this.book) {
        this.$emit("character_run_input", null);
      }
    }
  }
};
</script>
