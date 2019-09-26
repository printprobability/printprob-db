<template>
  <b-form-group
    id="character-run-group"
    label-for="character-run-select"
    label="Created by character run"
  >
    <b-form-select
      id="character-run-select"
      class="my-2"
      v-model="selected_character_run"
      :options="character_runs"
      @input="$emit('input', selected_character_run)"
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
      type: Number,
      default: null
    }
  },
  data() {
    return {
      selected_character_run: null,
      character_runs: []
    };
  },
  methods: {
    get_character_runs: function() {
      return HTTP.get("/character_runs/").then(
        response => {
          var character_run_options = _.concat(
            {
              text: "All character_runs",
              value: null
            },
            response.data.results.map(x => {
              return x.book.eebo + " - " + x.date_stared;
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
  mounted() {
    this.get_character_runs();
    this.selected_character_run = this.value;
  }
};
</script>