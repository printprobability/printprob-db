<template>
  <div class="container-fluid">
    <h1>Review character quality</h1>
    <b-toast variant="success" id="success_toast">Characters updated</b-toast>
    <b-row>
      <div class="col-7">
        <b-alert variant="warning" show
          >Do not change filter settings if you have any pending annotations.
          Make sure to commit the annotations to the database first.</b-alert
        >
        <CharacterList
          @update="update_displayed_images"
          @char_clicked="toggle_character"
          :good_characters="good_characters"
          :bad_characters="bad_characters"
          :page="page"
          @page_input="page = $event"
          :character_class="character_class"
          @character_class_input="character_class = $event"
          :book="book"
          @book_input="book = $event"
          :char_agreement="char_agreement"
          @char_agreement_input="char_agreement = $event"
          :order="order"
          @order_input="order = $event"
          :character_run="character_run"
          @character_run_input="character_run = $event"
          v-model="displayed_images"
          :key="char_list_key"
        />
      </div>
      <div class="col-5">
        <div class="card sticky-top">
          <div class="card-body">
            <CharacterClassSelect
              v-model="new_class"
              label="Replacement class"
              description="New class to replace the machine assignment"
            />
            <b-button
              block
              :title="null_title"
              @click="nullify"
              variant="secondary"
              >Null all</b-button
            >
            <b-button
              block
              :title="accept_title"
              @click="mark_all_correct"
              variant="success"
              >Accept all</b-button
            >
            <b-button
              block
              :disabled="!new_class"
              :title="replace_title"
              @click="mark_all_replace"
              variant="warning"
              >Replace all</b-button
            >
            <b-button
              block
              :title="commit_title"
              :disabled="disable_commit"
              @click="commit_marks"
              variant="primary"
              >Commit to DB</b-button
            >
          </div>
        </div>
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
    CharacterClassSelect,
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
      order: "character_class",
      character_run: null,
      char_agreement: "unknown",
      char_list_key: 0,
    };
  },
  computed: {
    good_characters() {
      return _.filter(
        this.displayed_images,
        (x) =>
          !!x.human_character_class &&
          x.character_class == x.human_character_class
      ).map((x) => x.id);
    },
    bad_characters() {
      return _.filter(
        this.displayed_images,
        (x) =>
          !!x.human_character_class &&
          x.character_class != x.human_character_class
      ).map((x) => x.id);
    },
    null_title() {
      return "Will mark all characters as having no human-assigned character class";
    },
    accept_title() {
      return "Will confirm all characters as having the class assigned to them on Bridges.";
    },
    replace_title() {
      return (
        "Will mark all characters as having the new class " + this.new_class
      );
    },
    commit_title() {
      return "Will commit the current changes to the database.";
    },
    view_params() {
      return {
        book: this.book,
        order: this.order,
        character_run: this.character_run,
        character_class: this.character_class,
        char_agreement: this.char_agreement,
      };
    },
  },
  methods: {
    update_displayed_images: function (imgs) {
      this.displayed_images = imgs;
      this.disable_commit = true;
    },
    toggle_character: function (id) {
      const i = _.findIndex(this.displayed_images, (x) => x.id == id);
      if (!this.displayed_images[i].human_character_class) {
        this.displayed_images[i].human_character_class = this.new_class;
      } else if (
        this.displayed_images[i].human_character_class !=
        this.displayed_images[i].character_class
      ) {
        this.displayed_images[i].human_character_class =
          this.displayed_images[i].character_class;
      } else {
        this.displayed_images[i].human_character_class = this.new_class;
      }
      this.disable_commit = false;
    },
    mark_all_correct() {
      _.each(
        this.displayed_images,
        (x) => (x.human_character_class = x.character_class)
      );
      this.disable_commit = false;
    },
    mark_all_replace() {
      _.each(
        this.displayed_images,
        (x) => (x.human_character_class = this.new_class)
      );
      this.disable_commit = false;
    },
    nullify() {
      _.each(this.displayed_images, (x) => (x.human_character_class = null));
      this.disable_commit = false;
    },
    refresh_cl() {},
    commit_marks() {
      const updates = _.groupBy(this.displayed_images, "human_character_class");
      console.log(updates);
      _.forEach(updates, (g, k) => {
        const ids = g.map((x) => x.id);
        var hcc = k == "null" ? null : k;
        const payload = {
          characters: ids,
          human_character_class: hcc,
        };
        console.log(payload);
        return HTTP.post("/characters/annotate/", payload).then(
          (response) => {
            console.log(response);
          },
          (error) => {
            console.log(error);
          }
        );
      });
      this.$bvToast.show("success_toast");
      this.char_list_key += 1;
    },
  },
  created() {
    this.book = this.$route.query.book;
    this.order = this.$route.query.order;
    this.character_run = this.$route.query.character_run;
    this.character_class = this.$route.query.character_class;
    this.char_agreement = this.$route.query.char_agreement;
  },
  updated() {
    this.$router.push({ name: "CharacterReviewView", query: this.view_params });
  },
};
</script>
