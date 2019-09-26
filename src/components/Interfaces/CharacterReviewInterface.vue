<template>
  <div class="container-fluid">
    <h1>Review character quality</h1>
    <CharacterList
      @update="update_displayed_images"
      @char_clicked="toggle_character"
      :good_characters="good_characters"
      :bad_characters="bad_characters"
    />
    <b-row class="d-flex align-items-center">
      <div class="col-4">
        <CharacterClassSelect
          v-model="new_class"
          label="Replacement class"
          description="New class to replace the machine assignment"
        />
      </div>
      <div class="col-2">
        <b-button block @click="reset" variant="secondary">Reset</b-button>
      </div>
      <div class="col-2">
        <b-button
          block
          v-b-tooltip.hover
          :title="accept_title"
          @click="mark_all_correct"
          variant="success"
        >Accept all</b-button>
      </div>
      <div class="col-2">
        <b-button
          block
          :disabled="!new_class"
          v-b-tooltip.hover
          :title="replace_title"
          @click="mark_all_replace"
          variant="warning"
        >Replace all</b-button>
      </div>
      <div class="col-2">
        <b-button
          block
          :disabled="disable_commit"
          @click="commit_marks"
          variant="primary"
        >Commit to DB</b-button>
      </div>
    </b-row>
  </div>
</template>

<script>
import CharacterList from "../Characters/CharacterList";
import CharacterClassSelect from "../Menus/CharacterClassSelect";
import _ from "lodash";

export default {
  name: "CharacterReviewInterface",
  components: {
    CharacterList,
    CharacterClassSelect
  },
  props: {
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
  data() {
    return {
      new_class: null,
      displayed_images: [],
      good_characters: [],
      bad_characters: []
    };
  },
  computed: {
    accept_title() {
      return (
        "Will confirm all characters as having the class " +
        this.character_class +
        " (the machine-assigned class)"
      );
    },
    replace_title() {
      return (
        "Will mark all characters as having the new class " + this.new_class
      );
    },
    disable_commit() {
      return this.good_characters.length < 1 && this.bad_characters.length < 1;
    }
  },
  methods: {
    update_displayed_images: function(imgs) {
      this.displayed_images = imgs;
    },
    toggle_character: function(id) {
      console.log(id);
      if (this.good_characters.includes(id)) {
        this.good_characters = _.difference(this.good_characters, [id]);
        this.bad_characters = _.union(this.bad_characters, [id]);
      } else if (this.bad_characters.includes(id)) {
        this.bad_characters = _.difference(this.bad_characters, [id]);
        this.good_characters = _.union(this.good_characters, [id]);
      } else {
        this.good_characters = _.union(this.good_characters, [id]);
      }
    },
    mark_all_correct() {
      this.good_characters = this.displayed_images.map(x => x.id);
      this.bad_characters = [];
    },
    mark_all_replace() {
      this.bad_characters = this.displayed_images.map(x => x.id);
      this.good_characters = [];
    },
    reset() {
      this.bad_characters = [];
      this.good_characters = [];
    },
    commit_marks() {}
  }
};
</script>
