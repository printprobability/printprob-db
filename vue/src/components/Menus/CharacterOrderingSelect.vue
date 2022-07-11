<template>
  <b-form-group id="ordering-group" label="Sort by" label-size="sm">
    <b-form-select size="sm" id="ordering-select" :value="value" :options="options" @input="$emit('input', $event)" />
  </b-form-group>
</template>

<script>
export default {
  name: "CharacterOrderingSelect",
  props: {
    value: {
      type: String,
      default: "character_class",
    },
  },
  data() {
    return {
      options: [
        {
          value: "-damage_score",
          text: "Damage score (descending)",
        },
        {
          value: "damage_score",
          text: "Damage score (ascending)",
        },
        {
          value: "-class_probability",
          text: "Probability (descending)",
        },
        {
          value: "class_probability",
          text: "Probability (ascending)",
        },
        {
          value: "bookseq,pageseq,lineseq,sequence",
          text: "Sequence",
        },
        {
          value: "character_class",
          text: "Character class"
        }
      ],
    };
  },
};
</script>
