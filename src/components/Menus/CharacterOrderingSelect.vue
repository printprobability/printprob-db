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
  data() {
    return {
      options: [
        {
          value: null,
          text: "created"
        },
        {
          value: "class_probability",
          text: "Probability (ascending)"
        },
        {
          value: "-class_probability",
          text: "Probability (descending)"
        }
      ],
      value: null
    };
  }
};
</script>