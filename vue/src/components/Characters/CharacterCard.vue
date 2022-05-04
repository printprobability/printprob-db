<template>
  <div>
    <p>
      Machine: {{ character.character_class }} ({{
        (character.class_probability * 100).toFixed(2)
      }}%)
    </p>
    <p>Human: {{ character.human_character_class }}</p>
    <p v-if="character.damage_score">
      Damage score: {{ character.damage_score }}
    </p>
    <p>
      <router-link :to="character_link" target="_blank" rel="noopen noreferrer">
        <img class="buffer_preview" :src="character.image.buffer" />
      </router-link>
    </p>
    <router-link :to="character_link" target="_blank" rel="noopen noreferrer"
      >See character in context</router-link
    >
  </div>
</template>

<script>
export default {
  name: "CharacterCard",
  props: {
    character: Object,
  },
  computed: {
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
