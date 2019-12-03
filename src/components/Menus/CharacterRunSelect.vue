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
      type: String,
      default: null
    }
  },
  data() {
    return {};
  },
  asyncComputed: {
    character_runs() {
      return HTTP.get("/runs/characters/", {
        params: { book: this.book }
      }).then(
        response => {
          return response.data.results.map(x => {
            return {
              text: x.date_started,
              value: x.id
            };
          });
        },
        error => {
          console.log(error);
        }
      );
    }
  }
};
</script>