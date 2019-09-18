<template>
  <img
    :src="character.image.web_url"
    class="character-image my-1 mx-auto"
    v-b-tooltip.hover
    :title="character_tooltip"
  />
</template>

<script>
export default {
  name: "CharacterImage",
  props: {
    character: Object
  },
  computed: {
    character_tooltip: function() {
      return this.character.label;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.character-image {
  max-width: 100px;
  border: 2px solid black;
}
</style>
