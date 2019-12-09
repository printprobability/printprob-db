<template>
  <b-form-select
    v-if="!!character_groupings"
    class="my-2"
    :value="value"
    :options="character_groupings"
    @input="$emit('input', $event)"
  />
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterGroupingSelect",
  props: {
    value: String
  },
  data() {
    return {};
  },
  asyncComputed: {
    character_groupings() {
      return HTTP.get("/character_groupings/").then(
        response => {
          return _.concat(
            {
              text: "Select character grouping",
              value: null
            },
            response.data.results.map(x => {
              return { value: x.id, text: x.label };
            })
          );
        },
        error => {
          console.log(error);
        }
      );
    }
  }
};
</script>