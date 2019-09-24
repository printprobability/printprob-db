<template>
  <b-form-group
    id="bad-character-group"
    label="Show bad characters?"
    description="Characters marked bad by a human reviewer"
  >
    <b-form-radio v-model="value" name="bad-character-include" value="null">Show all</b-form-radio>
    <b-form-radio v-model="value" name="bad-character-show" value="true">Show only bad</b-form-radio>
    <b-form-radio v-model="value" name="bad-character-exclude" value="false">Show only good</b-form-radio>
  </b-form-group>
</template>

<script>
export default {
  name: "BadCharacterRadio",
  data() {
    return {
      value: null
    };
  },
  watch: {
    value() {
      this.$emit("input", this.value);
    }
  }
};
</script>