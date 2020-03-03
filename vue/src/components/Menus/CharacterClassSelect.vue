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
      const group_dict = {
        cl: "Lowercase",
        cu: "Uppercase",
        pu: "Puncutation",
        nu: "Number"
      };

      return HTTP.get("/character_classes/", { params: { limit: 200 } }).then(
        response => {
          const null_value = { text: "all characters", value: null };
          const grouped_classes = _.groupBy(response.data.results, "group");

          const formatted_classes = _.sortBy(
            _.map(grouped_classes, (x, n) => {
              return {
                label: group_dict[n],
                options: _.map(x, t => {
                  return { value: t.classname, text: t.label };
                })
              };
            }),
            "label"
          );

          var character_options = _.concat(null_value, formatted_classes);
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