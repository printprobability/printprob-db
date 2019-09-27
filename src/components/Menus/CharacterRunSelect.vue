<template>
  <b-form-group
    id="character-run-group"
    label-for="character-run-select"
    label="Created by character run"
  >
    <b-form-select
      id="character-run-select"
      class="my-2"
      :value="value"
      :options="character_runs"
      @input="$emit('input', $event)"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

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
          var character_run_options = _.concat(
            {
              text: "All character runs",
              value: null
            },
            response.data.results.map(x => {
              return {
                text: x.book.label + " - " + x.date_stared,
                value: x.id
              };
            })
          );
          this.character_runs = character_run_options;
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