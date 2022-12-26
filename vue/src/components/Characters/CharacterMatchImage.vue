<template>
  <div>
    <span>{{ name }}</span>
    <CharacterImage
      :key="index + name"
      :character="character"
      image_size="bound100"
      :selected="is_match_image && is_char_selected"
      :parentComponent="parentComponent(index, col_index)"
      @char_clicked="
        is_match_image &&
          $emit('char_clicked', { id: character.id, row_idx: index - 1 })
      "
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
    is_match_image: Boolean,
    col_index: Number,
    character_row: Object,
    selected: Object,
  },
  computed: {
    is_char_selected() {
      return (
        this.selected && this.selected[this.index - 1] === this.character.id
      )
    },
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
  },
}
</script>

<style>
span {
  display: inline-block;
  word-break: break-word;
}
</style>
