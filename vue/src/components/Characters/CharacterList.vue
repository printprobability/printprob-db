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
          <div class="col-8">
            <p v-if="!!book">
              <b-button @click="clear_book" variant="danger" size="sm"
                >x</b-button
              >
              <strong>Book:</strong>
              {{ book_title }}
            </p>
            <BookAutocomplete
              v-else
              :value="book"
              @input="$emit('book_input', $event)"
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
            <CharacterOrderingSelect
              :value="order"
              @input="$emit('order_input', $event)"
            />
          </div>
        </b-row>
      </div>
    </div>
    <div class="char-images card my-2">
      <div class="card-header">
        <Spinner v-if="progress_spinner" />
        <div class="paginator" v-if="value.length > 0">
          <p>
            Characters {{ 1 + (page - 1) * $APIConstants.REST_PAGE_SIZE }} to
            {{ (page - 1) * $APIConstants.REST_PAGE_SIZE + value.length }}
            <span
              v-if="results.next"
              v-b-tooltip.hover
              title="Arbitrarily counting characters is a very expensive operation, so we only estimate here..."
              >(out of many)</span
            >
          </p>
          <b-pagination
            hide-goto-end-buttons
            v-show="pagination_needed"
            v-model="page"
            :per-page="$APIConstants.REST_PAGE_SIZE"
            :total-rows="mock_rows"
            aria-controls="character-results"
            limit="3"
          />
          <b-form-group label="Image size">
            <b-form-radio v-model="image_size" name="image-size" value="actual"
              >Actual pixels</b-form-radio
            >
            <b-form-radio
              v-model="image_size"
              name="image-size"
              value="bound100"
              >100px</b-form-radio
            >
            <b-form-radio
              v-model="image_size"
              name="image-size"
              value="bound300"
              >300px</b-form-radio
            >
          </b-form-group>
        </div>
        <div show v-else>No matching characters</div>
      </div>
      <div
        class="d-flex flex-wrap card-body"
        id="character-results"
        v-if="value.length > 0"
      >
        <CharacterImage
          v-for="character in value"
          :character="character"
          :key="character.id"
          :highlight="highlighted_characters.includes(character.id)"
          :bad="bad_characters.includes(character.id)"
          :good="good_characters.includes(character.id)"
          :image_size="image_size"
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
import CharacterImage from "./CharacterImage";
import Spinner from "../Interfaces/Spinner";
import { HTTP } from "../../main";

export default {
  name: "CharacterList",
  props: {
    highlighted_characters: {
      type: Array,
      default: function () {
        return [];
      },
    },
    bad_characters: {
      type: Array,
      default: function () {
        return [];
      },
    },
    good_characters: {
      type: Array,
      default: function () {
        return [];
      },
    },
    character_class: {
      default: null,
      type: String,
    },
    book: {
      default: null,
      type: String,
    },
    char_agreement: {
      default: "all",
      type: String,
    },
    order: {
      default: "-class_probability",
      type: String,
    },
    value: {
      // Here is where the characters themselves live
      type: Array,
      default: () => [],
    },
  },
  components: {
    CharacterClassSelect,
    CharacterOrderingSelect,
    BookAutocomplete,
    CharacterAgreementRadio,
    CharacterImage,
    Spinner,
  },
  data() {
    return {
      progress_spinner: false,
      cursor: null,
      page: 1,
      image_size: "actual",
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
          agreement: this.char_agreement,
          ordering: this.order,
        },
      }).then(
        (response) => {
          this.progress_spinner = false;
          return response.data;
        },
        (error) => {
          this.progress_spinner = false;
          console.log(error);
        }
      );
    },
    book_title() {
      if (!!this.book) {
        return HTTP.get("/books/" + this.book + "/").then(
          (results) => {
            return results.data.label;
          },
          (error) => {
            console.log(error);
          }
        );
      }
    },
  },
  computed: {
    view_params() {
      return {
        limit: this.$APIConstants.REST_PAGE_SIZE,
        character_class: this.character_class,
        book: this.book,
        agreement: this.char_agreement,
        order: this.order,
        cursor: this.cursor,
      };
    },
    rest_offset: function () {
      return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE;
    },
    pagination_needed: function () {
      return !!this.results.next || !!this.results.previous;
    },
    mock_rows: function () {
      var baseline = this.rest_offset + this.value.length;
      if (!!this.results.next) {
        baseline += this.$APIConstants.REST_PAGE_SIZE;
      }
      return baseline;
    },
  },
  methods: {
    clear_book() {
      this.$emit("book_input", null);
    },
  },
  watch: {
    results() {
      this.$emit("input", this.results.results);
    },
    view_params() {
      this.page = 1;
    },
  },
};
</script>
