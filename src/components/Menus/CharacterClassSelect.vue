<template>
  <b-form-select
    class="my-2"
    v-model="selected_character_class"
    :options="character_classes"
    @input="select_class"
  ></b-form-select>
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterClassSelect",
  props: {
    selected_character_class: null
  },
  data() {
    return {
      // selected_character_class: null,
      character_classes: []
    };
  },
  methods: {
    get_charcacter_classes: function() {
      return HTTP.get("/character_classes/").then(
        response => {
          var character_options = _.concat(
            { text: "Select a character class", value: null },
            response.data.results.map(x => x.classname)
          );
          this.character_classes = character_options;
        },
        error => {
          console.log(error);
        }
      );
    },
    select_class: function() {
      this.$emit("selected", this.selected_character_class);
    }
  },
  created() {
    this.get_charcacter_classes();
  }
};
</script>