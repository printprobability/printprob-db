<template>
  <b-form-group
    id="character-run-group"
    label-for="character-run-select"
    label="Created by character run"
    description="Show only characters from a particular run from the selected book."
  >
    <b-form-select
      id="character-run-select"
      :value="value"
      :options="character_runs"
      @input="$emit('input', $event)"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from "../../main";

export default {
  name: "CharacterRunSelect",
  props: {
    value: {
      type: String,
      default: null
    },
    book: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      character_runs: []
    };
  },
  methods: {
    get_character_runs: function() {
      return HTTP.get("/runs/characters/", {
        params: { book: this.book }
      }).then(
        response => {
          this.character_runs = response.data.results.map(x => {
            return {
              text: x.date_started,
              value: x.id
            };
          });
          this.$emit("input", this.character_runs[0].value);
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  created() {
    this.get_character_runs();
  }
};
</script>