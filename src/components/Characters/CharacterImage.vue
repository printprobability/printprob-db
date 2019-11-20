<template>
  <div>
    <img
      :id="character.id"
      :src="character.image.web_url"
      class="character-image m-1"
      @click="$emit('char_clicked', character.id)"
      :class="{ highligted: highlight, marked_good: good, marked_bad: bad }"
    />
    <b-popover
      :target="character.id"
      :title="character.label"
      triggers="hover"
      placement="top"
      :delay="pop_delay"
    >
      <p>Machine: {{ character.character_class }} ({{ (character.class_probability * 100).toFixed(2) }}%)</p>
      <p>Human: {{ character.human_character_class }}</p>
      <p>
        <img :src="character.image.buffer" />
      </p>
      <router-link :to="character_link">See character in context</router-link>
    </b-popover>
  </div>
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
  data() {
    return {
      pop_delay: { show: 750, hide: 500 }
    };
  },
  computed: {
    character_tooltip() {
      return (
        this.character.label +
        "hu class: " +
        this.character.human_character_class
      );
    },
    character_link() {
      return {
        name: "CharacterDetailView",
        params: {
          id: this.character.id
        }
      };
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
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(180deg);
}

img.marked_bad {
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(320deg);
}

img.marked_good {
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(70deg);
}
</style>
