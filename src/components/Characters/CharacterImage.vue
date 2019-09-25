<template>
  <img
    :src="character.image.web_url"
    class="character-image m-1"
    @click="$emit('char_clicked', character.id)"
    v-b-tooltip.hover
    :title="character_tooltip"
    :class="{ highligted: highlight, bad: bad, bad: character.bad }"
  />
</template>

<script>
export default {
  name: "CharacterImage",
  props: {
    character: Object,
    highlight: Boolean,
    bad: Boolean
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
  max-height: 100px;
  border: 1px solid black;
}

img.highligted {
  border: 5px solid rgb(163, 163, 238);
}

img.bad {
  border: 5px solid red;
  filter: invert(100%);
}
</style>
