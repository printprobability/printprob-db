<template>
  <b-form-group
    id="show-damaged-characters-group"
    label="Show only damage-scored characters?"
    description="Only show characters that have been assigned a damage score?"
    label-size="sm"
  >
    <b-form-checkbox size="sm" v-model="checked" name="show-damaged-characters">
    </b-form-checkbox>
  </b-form-group>
</template>

<script>
export default {
  name: 'ShowDamagedCharactersCheckbox',
  props: {
    value: Boolean,
  },
  data() {
    return {
      checked: this.value,
    }
  },
  watch: {
    checked() {
      this.$emit('input', this.checked)
    },
  },
}
</script>
