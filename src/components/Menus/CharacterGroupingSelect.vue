<template>
  <b-form-select
    class="my-2"
    v-model="value"
    :options="character_groupings"
    @input="select_character_grouping"
  ></b-form-select>
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
    return {
      character_groupings: []
    };
  },
  methods: {
    get_character_groupings: function() {
      return HTTP.get("/character_groupings/").then(
        response => {
          var cg_options = _.concat(
            {
              text: "Select character grouping",
              value: null
            },
            response.data.results.map(x => {
              return { value: x.id, text: x.label };
            })
          );
          this.character_groupings = cg_options;
        },
        error => {
          console.log(error);
        }
      );
    },
    select_character_grouping: function() {
      this.$emit("input", this.value);
    }
  },
  created() {
    this.get_character_groupings();
  }
};
</script>