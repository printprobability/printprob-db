<template>
  <img
    :src="character.image.web_url"
    class="character-image m-1"
    @click="$emit('char_clicked', character.id)"
    v-b-tooltip.hover
    :title="character_tooltip"
    :class="{ highligted: highlight, marked_good: good, marked_bad: bad }"
  />
</template>

<script>
export default {
  name: "CharacterImage",
  props: {
    character: Object,
    highlight: Boolean,
    bad: Boolean,
    good: Boolean
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
.overlay {
  z-index: 10;
}

.overlay.highlighted {
  color: rgba(247, 244, 112);
}

.overlay.marked_bad {
  background: rgba(255, 0, 0, 0.5);
}

.overlay.marked_good {
  background: rgba(0, 128, 0, 0.5);
}

img.character-image {
  max-width: 100px;
  max-height: 100px;
  border: 1px solid black;
}

img.highligted {
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(180deg);
}

img.marked_bad {
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(320deg);
}

img.marked_good {
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(70deg);
}
</style>
