<template>
  <b-form-group
    id="character-class-group"
    label-for="character-class-select"
    :label="label"
    :description="description"
    label-size="sm"
  >
    <b-form-select
      size="sm"
      id="character-class-id"
      :value="value"
      :options="character_classes"
      @input="$emit('input', $event)"
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
    },
    label: {
      default: "Character Class",
      type: String
    },
    description: {
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
  created() {
    this.get_charcacter_classes();
  }
};
</script>