<template>
  <b-form-group id="ordering-group" label="Sort by" label-size="sm">
    <b-form-select
      size="sm"
      id="ordering-select"
      :value="value"
      :options="options"
      @input="$emit('input', $event)"
    />
  </b-form-group>
</template>

<script>
export default {
  name: "CharacterOrderingSelect",
  props: {
    value: {
      type: String,
      default: "-class_probability",
    },
  },
  data() {
    return {
      options: [
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
      ],
    };
  },
};
</script>
