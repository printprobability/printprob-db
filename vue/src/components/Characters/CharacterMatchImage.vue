<template>
  <div>
    <span>{{ name }}</span>
    <CharacterImage
      :key="index + name"
      :character="character"
      image_size="bound100"
      :parentComponent="parentComponent(index, col_index)"
    />
    <span v-if="distance">{{ distance }}</span>
  </div>
</template>

<script>
import CharacterImage from './CharacterImage'

export default {
  name: 'CharacterMatchImage',
  components: {
    CharacterImage,
  },
  props: {
    index: Number,
    col_index: Number,
    character_row: Object,
  },
  data() {
    return {
      name: this.character_row['name'],
      character: this.character_row['obj'],
      distance: this.character_row['distance'],
    }
  },
  methods: {
    parentComponent(row, col) {
      if (col === undefined) {
        return `character_match_${row}`
      }
      return `character_match_${row}_${col}`
    },
    onCharacterSelection() {
      this.$emit('char_clicked', this.character.id)
    },
  },
}
</script>

<style>
span {
  display: inline-block;
  word-break: break-word;
}
</style>
