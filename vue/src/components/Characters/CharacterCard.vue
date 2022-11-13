<template>
  <div>
    <p>
      Printer:
      {{ character.book.pp_printer || character.book.colloq_printer }}
    </p>
    <p>
      Published:
      {{ character.book.pq_year_early || character.book.tx_year_early }}
    </p>
    <p v-if="character.damage_score >= 0">
      Damage score: {{ character.damage_score }}
    </p>
    <p>
      Machine: {{ character.character_class }} ({{
        (character.class_probability * 100).toFixed(2)
      }}%)
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
  name: 'CharacterCard',
  props: {
    character: Object,
  },
  computed: {
    character_link() {
      return {
        name: 'CharacterDetailView',
        params: {
          id: this.character.id,
        },
      }
    },
  },
}
</script>
