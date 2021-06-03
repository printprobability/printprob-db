<template>
  <div>
    <img
      :id="character.id"
      :src="character.image.web_url"
      class="character-image m-1"
      @click="$emit('char_clicked', character.id)"
      :class="{
        highligted: highlight,
        marked_good: good,
        marked_bad: bad,
        actual: size_actual,
        bound100: size_bound100,
        bound300: size_bound300,
      }"
      @mouseover="$emit('hover', $event)"
    />
    <b-popover
      :target="character.id"
      :title="character.label"
      triggers="hover"
      placement="top"
      :delay="pop_delay"
    >
      <CharacterCard :character="character" />
    </b-popover>
  </div>
</template>

<script>
import CharacterCard from "./CharacterCard";
export default {
  name: "CharacterImage",
  components: {
    CharacterCard,
  },
  props: {
    character: Object,
    highlight: Boolean,
    bad: Boolean,
    good: Boolean,
    image_size: String,
    popover: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      pop_delay: { show: 1000, hide: 200 },
    };
  },
  computed: {
    size_actual() {
      return this.image_size == "actual";
    },
    size_bound100() {
      return this.image_size == "bound100";
    },
    size_bound300() {
      return this.image_size == "bound300";
    },
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
          id: this.character.id,
        },
      };
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.character-image {
  border: 1px solid black;
}

img.actual {
}

img.bound100 {
  max-width: 100px;
  max-height: 100px;
  min-height: 100px;
}

img.bound300 {
  max-width: 300px;
  max-height: 300px;
  min-height: 300px;
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

img.buffer_preview {
  border: 1px solid black;
}
</style>
