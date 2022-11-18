<template>
  <div>
    <img
      :id="parentComponent + '_' + character.id"
      :src="character.image.web_url"
      class="character-image m-1"
      @click="onCharacterSelection"
      v-on:dblclick="$emit('char_double_clicked', character.id)"
      :class="{
        highligted: highlight,
        marked_good: good,
        marked_bad: bad,
        actual: size_actual,
        bound100: size_bound100,
        bound300: size_bound300,
        selected: isCharSelected,
      }"
      @mouseover="onCharacterHover"
    />
    <b-popover
      :target="parentComponent + '_' + character.id"
      :title="character.label"
      triggers="hover"
      placement="top"
      :delay="pop_delay"
      @hidden="onHidden"
    >
      <CharacterCard
        v-if="hoveredCharacter !== null"
        :character="hoveredCharacter"
      />
    </b-popover>
  </div>
</template>

<script>
import CharacterCard from './CharacterCard'
import { HTTP } from '@/main'
import { debounce } from 'lodash'
export default {
  name: 'CharacterImage',
  components: {
    CharacterCard,
  },
  props: {
    parentComponent: {
      type: String,
    },
    editMode: {
      type: Boolean,
      default: false,
    },
    character: Object,
    highlight: Boolean,
    bad: Boolean,
    good: Boolean,
    image_size: String,
    popover: {
      type: Boolean,
      default: false,
    },
    selected: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      pop_delay: { show: 1000, hide: 200 },
      hoveredCharacter: null,
    }
  },
  computed: {
    size_actual() {
      return this.image_size == 'actual'
    },
    size_bound100() {
      return this.image_size == 'bound100'
    },
    size_bound300() {
      return this.image_size == 'bound300'
    },
    character_tooltip() {
      return (
        this.character.label +
        'hu class: ' +
        this.character.human_character_class
      )
    },
    character_link() {
      return {
        name: 'CharacterDetailView',
        params: {
          id: this.character.id,
        },
      }
    },
    isCharSelected() {
      return this.selected
    },
  },
  methods: {
    onCharacterSelection() {
      this.$emit('char_clicked', this.character.id)
    },
    onCharacterHover: debounce(function (event) {
      HTTP.get('/characters/' + this.character.id + '/').then(
        (response) => {
          this.hoveredCharacter = response.data
          this.$emit('hover', event)
        },
        (error) => {
          this.hoveredCharacter = null
          console.log(error)
        }
      )
    }, 500),
    onHidden() {
      this.hoveredCharacter = null
    },
  },
}
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

img.selected {
  filter: sepia(100%) saturate(300%) brightness(70%) hue-rotate(180deg);
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
