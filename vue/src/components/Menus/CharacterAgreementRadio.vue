<template>
  <b-form-group
    id="character-agreement-group"
    label="Class agreement?"
    description="Do human reviewers agree with machine classification?"
    label-size="sm"
  >
    <b-form-radio
      size="sm"
      v-model="selectedOption"
      name="character-agreement"
      value="all"
      >Show all</b-form-radio
    >
    <b-form-radio
      size="sm"
      v-model="selectedOption"
      name="character-agreement"
      value="unknown"
      >No human classification yet</b-form-radio
    >
    <b-form-radio
      size="sm"
      v-model="selectedOption"
      name="character-agreement"
      value="disagreement"
      >Disagreements only</b-form-radio
    >
    <b-form-radio
      size="sm"
      v-model="selectedOption"
      name="character-agreement"
      value="agreement"
      >Agreements only</b-form-radio
    >
  </b-form-group>
</template>

<script>
export default {
  name: 'CharacterAgreementRadio',
  props: {
    value: String,
  },
  data() {
    return {
      selectedOption: this.value,
    }
  },
  watch: {
    selectedOption() {
      this.$emit('input', this.selectedOption)
    },
  },
}
</script>
