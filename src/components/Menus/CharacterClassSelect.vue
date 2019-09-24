<template>
  <b-form-group
    id="character-class-group"
    label-for="character-class-select"
    label="Character class"
  >
    <b-form-select
      id="character-class-id"
      v-model="selected_character_class"
      :options="character_classes"
      @input="$emit('input', selected_character_class)"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterClassSelect",
  props: {
    value: {
      default: null,
      type: String
    }
  },
  data() {
    return {
      selected_character_class: null,
      character_classes: []
    };
  },
  methods: {
    get_charcacter_classes: function() {
      return HTTP.get("/character_classes/").then(
        response => {
          var character_options = _.concat(
            { text: "all characters", value: null },
            response.data.results.map(x => x.classname)
          );
          this.character_classes = character_options;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  created() {
    this.get_charcacter_classes();
    this.selected_character_class = this.value;
  }
};
</script>