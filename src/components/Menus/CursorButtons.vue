<template>
  <b-button-group>
    <b-button :disabled="!prev" @click="$emit('cursor', prev)">Previous</b-button>
    <b-button :disabled="!next" @click="$emit('cursor', next)">Next</b-button>
  </b-button-group>
</template>

<script>
export default {
  name: "CursorButtons",
  props: {
    prev: {
      type: String,
      default: null
    },
    next: {
      type: String,
      default: null
    }
  }
};
</script>