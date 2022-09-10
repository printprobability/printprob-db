<template>
  <b-form-select
    v-if="!!character_groupings"
    class="my-2"
    :value="value"
    :options="character_groupings"
    @input="$emit('input', $event)"
  />
</template>

<script>
import { HTTP } from '../../main'
import _ from 'lodash'

export default {
  name: 'CharacterGroupingSelect',
  props: {
    value: String,
    label: {
      type: String,
      default: 'Select character grouping',
    },
    excludedCharacterGroup: String, // display options excluding this one
  },
  data() {
    return {}
  },
  asyncComputed: {
    character_groupings() {
      return HTTP.get('/character_groupings/', { params: { limit: 200 } }).then(
        (response) => {
          const result = _.concat(
            {
              text: this.label,
              value: null,
            },
            _.sortBy(
              response.data.results.map((x) => ({
                value: x.id,
                text: x.label,
              })),
              'text'
            )
          )
          return !!this.excludedCharacterGroup
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
  },
}
</script>
