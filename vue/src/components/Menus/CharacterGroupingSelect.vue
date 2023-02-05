<template>
  <b-form-group class="my-4">
    <VueBootstrapTypeahead
      class="auto_select"
      :minMatchingChars="min_matching_chars"
      :max-matches="max_matches"
      v-if="character_groupings.length"
      :data="character_groupings"
      :serializer="(item) => item.text"
      :value="value"
      :placeholder="label"
      @hit="$emit('input', $event.value)"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from '../../main'
import _ from 'lodash'
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'

export default {
  name: 'CharacterGroupingSelect',
  components: {
    VueBootstrapTypeahead,
  },
  props: {
    value: String,
    label: {
      type: String,
      default: 'Select character grouping',
    },
    excludedCharacterGroup: String, // display options excluding this one
  },
  data() {
    return {
      character_groupings: [],
      min_matching_chars: 1,
      max_matches: 1000,
    }
  },
  mounted() {
    HTTP.get('/character_groupings/', { params: { limit: 200 } }).then(
      (response) => {
        const result = _.sortBy(
          response.data.results.map((x) => ({
            value: x.id,
            text: x.label,
          })),
          'text'
        )
        this.character_groupings = !!this.excludedCharacterGroup
          ? result.filter(
              (option) => option.value !== this.excludedCharacterGroup
            )
          : result
      },
      (error) => {
        console.log(error)
      }
    )
  },
}
</script>

<style scoped>
.auto_select {
  width: 20em;
}
</style>
