<template>
  <b-form-select
    class="my-2"
    v-model="selected_character_grouping"
    :options="character_grouping"
    @input="select_character_grouping"
  ></b-form-select>
</template>

<script>
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterGroupingSelect",
  data() {
    return {
      selected_character_grouping: null,
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
            response.data.results.map(x => x.label)
          );
          this.character_groupings = cg_options;
        },
        error => {
          console.log(error);
        }
      );
    },
    select_character_grouping: function() {
      this.$emit("selected", this.selected_character_grouping);
    }
  },
  created() {
    this.get_character_groupings();
  }
};
</script>