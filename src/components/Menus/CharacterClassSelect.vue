<template>
  <b-form-group
    id="character-class-group"
    label-for="character-class-select"
    label="Character class"
  >
    <b-form-select
      id="character-class-id"
      v-model="value"
      :options="character_classes"
      @input="$emit('input', value)"
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
  mounted() {
    this.get_charcacter_classes();
  }
};
</script>