<template>
  <div class="container-fluid">
    <h1>Review character quality</h1>
    <b-alert
      variant="warning"
      show
    >Do not change filter settings if you have any pending annotations. Make sure to commit the annotations to the database first.</b-alert>
    <b-toast variant="success" id="success_toast">Characters updated</b-toast>
    <CharacterList
      @update="update_displayed_images"
      @char_clicked="toggle_character"
      :good_characters="good_characters"
      :bad_characters="bad_characters"
      :page="page"
      @page_input="page=$event"
      :character_class="character_class"
      @character_class_input="character_class=$event"
      :book="book"
      @book_input="book=$event"
      :char_agreement="char_agreement"
      @char_agreement_input="char_agreement=$event"
      :order="order"
      @order_input="order=$event"
      :character_run="character_run"
      @character_run_input="character_run=$event"
      v-model="displayed_images"
      :key="char_list_key"
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
        <b-button block @click="nullify" variant="secondary">Null all</b-button>
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
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterReviewInterface",
  components: {
    CharacterList,
    CharacterClassSelect
  },
  data() {
    return {
      new_class: null,
      displayed_images: [],
      disable_commit: true,
      cl_key: 1,
      page: 1,
      character_class: null,
      book: null,
      order: "-class_probability",
      character_run: null,
      char_agreement: "all",
      char_list_key: 0
    };
  },
  computed: {
    good_characters() {
      return _.filter(
        this.displayed_images,
        x =>
          !!x.human_character_class &&
          x.character_class == x.human_character_class
      ).map(x => x.id);
    },
    bad_characters() {
      return _.filter(
        this.displayed_images,
        x =>
          !!x.human_character_class &&
          x.character_class != x.human_character_class
      ).map(x => x.id);
    },
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
    }
  },
  methods: {
    update_displayed_images: function(imgs) {
      this.displayed_images = imgs;
      this.disable_commit = true;
    },
    toggle_character: function(id) {
      const i = _.findIndex(this.displayed_images, x => x.id == id);
      if (!this.displayed_images[i].human_character_class) {
        this.displayed_images[i].human_character_class = this.new_class;
      } else if (
        this.displayed_images[i].human_character_class !=
        this.displayed_images[i].character_class
      ) {
        this.displayed_images[i].human_character_class = this.displayed_images[
          i
        ].character_class;
      } else {
        this.displayed_images[i].human_character_class = this.new_class;
      }
      this.disable_commit = false;
    },
    mark_all_correct() {
      _.each(
        this.displayed_images,
        x => (x.human_character_class = x.character_class)
      );
      this.disable_commit = false;
    },
    mark_all_replace() {
      _.each(
        this.displayed_images,
        x => (x.human_character_class = this.new_class)
      );
      this.disable_commit = false;
    },
    nullify() {
      _.each(this.displayed_images, x => (x.human_character_class = null));
      this.disable_commit = false;
    },
    refresh_cl() {},
    commit_marks() {
      const updates = _.groupBy(this.displayed_images, "human_character_class");
      console.log(updates);
      _.forEach(updates, (g, k) => {
        const ids = g.map(x => x.id);
        var hcc = k == "null" ? null : k;
        const payload = {
          characters: ids,
          human_character_class: hcc
        };
        console.log(payload);
        return HTTP.post("/characters/annotate/", payload).then(
          response => {
            console.log(response);
            this.$bvToast.show("success_toast");
            this.char_list_key += 1;
          },
          error => {
            console.log(error);
          }
        );
      });
    }
  },
  created() {
    this.book = this.$route.query.book;
    this.character_run = this.$route.query.character_run;
  }
};
</script>
