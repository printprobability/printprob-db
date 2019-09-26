<template>
  <b-form-group id="ordering-group" label="Sort by">
    <b-form-select
      id="ordering-select"
      v-model="value"
      :options="options"
      @input="$emit('input', value)"
    />
  </b-form-group>
</template>

<script>
export default {
  name: "CharacterOrderingSelect",
  props: {
    value: {
      type: String,
      default: "-class_probability"
    }
  },
  data() {
    return {
      options: [
        {
          value: "-class_probability",
          text: "Probability (descending)"
        },
        {
          value: "class_probability",
          text: "Probability (ascending)"
        }
      ]
    };
  }
};
</script>
