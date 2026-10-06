<template>
  <div v-if="character">
    <CharacterImage
      :key="index + name"
      :character="character"
      :image_size="image_size"
      :selected="is_match_image && is_char_selected"
      :parentComponent="parentComponent(index, col_index)"
      @char_clicked="
        is_match_image &&
          $emit('char_clicked', { id: character.id, row_idx: index - 1 })
      "
    />
    <span>{{ name }}</span>
    <span v-if="distance" class="d-block small">
      <template v-if="is_match_image">rank {{ col_index }} · </template>d={{
        distance
      }}
    </span>
    <span
      class="d-block small text-muted match-caption"
      :title="character.label"
      >{{ caption }}</span
    >
  </div>
</template>

<script>
import CharacterImage from './CharacterImage'
import { shortCharacterLabel } from '@/utils/matchRuns'

export default {
  name: 'CharacterMatchImage',
  components: {
    CharacterImage,
  },
  props: {
    index: Number,
    is_match_image: Boolean,
    col_index: String,
    character_row: Object,
    selected: Array,
    image_size: {
      type: String,
      default: 'bound100',
    },
  },
  computed: {
    caption() {
      return shortCharacterLabel(this.character.label)
    },
    is_char_selected() {
      return this.selected[this.index - 1].has(this.character.id)
    },
  },
  data() {
    return {
      name: this.character_row['name'],
      character: this.character_row,
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
.match-caption {
  max-width: 11rem;
  line-height: 1.2;
}
</style>
