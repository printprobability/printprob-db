<template>
  <div>
    <span>{{ data['name'] }}</span>
    <CharacterImage
      :key="data.index + data['name']"
      :character="data['obj']"
      image_size="bound100"
      :parentComponent="parentComponent(data.index, undefined)"
    />
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
    data: Object,
  },
  data() {
    return {
      character: this.data['obj'],
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
