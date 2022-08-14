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
  },
  data() {
    return {}
  },
  asyncComputed: {
    character_groupings() {
      return HTTP.get('/character_groupings/', { params: { limit: 200 } }).then(
        (response) => {
          return _.concat(
            {
              text: 'Select character grouping',
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
        },
        (error) => {
          console.log(error)
        }
      )
    },
  },
}
</script>
