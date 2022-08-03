<template>
  <b-form-group
    id="show-damaged-characters-group"
    label="Show only damage-scored characters?"
    description="Only show characters that have been assigned a damage score?"
    label-size="sm"
  >
    <b-form-checkbox
      size="sm"
      :checked="value"
      name="show-damaged-characters"
      @input="$emit('input', $event)"
    >
    </b-form-checkbox>
  </b-form-group>
</template>

<script>
export default {
  name: 'ShowDamagedCharactersCheckbox',
  props: {
    value: Boolean,
  },
}
</script>
