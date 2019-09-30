<template>
  <b-form-group
    id="character-agreement-group"
    label="Class agreement?"
    description="Do human reviewers agree with machine classification?"
  >
    <b-form-radio v-model="value" name="character-agreement-include" value="all">Show all</b-form-radio>
    <b-form-radio
      v-model="value"
      name="character-agreement-show"
      value="unknown"
    >No human classification yet</b-form-radio>
    <b-form-radio
      v-model="value"
      name="character-agreement-show"
      value="disagreement"
    >Disagreements only</b-form-radio>
    <b-form-radio
      v-model="value"
      name="character-agreement-exclude"
      value="agreement"
    >Agreements only</b-form-radio>
  </b-form-group>
</template>

<script>
export default {
  name: "CharacterAgreementRadio",
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