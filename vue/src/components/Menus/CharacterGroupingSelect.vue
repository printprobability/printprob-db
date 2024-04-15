<template>
  <div class="ui vertical segment">
    <div class="flexbox">
      <div class="flex-content">
        <b-form-group class="my-4">
          <model-select
            class="auto_select"
            v-if="$asyncComputed.character_groupings.success"
            :options="character_groupings"
            v-model="value"
            :placeholder="label"
            @input="$emit('input', $event)"
          >
          </model-select>
        </b-form-group>
      </div>
    </div>
  </div>
</template>

<script>
import { HTTP } from '../../main'
import _ from 'lodash'
import { ModelSelect } from 'vue-search-select'
import 'vue-search-select/dist/VueSearchSelect.css'

export default {
  name: 'CharacterGroupingSelect',
  components: {
    ModelSelect,
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
      min_matching_chars: 1,
      max_matches: 1000,
    }
  },
  asyncComputed: {
    character_groupings() {
      return HTTP.get('/character_groupings/', { params: { limit: 500 } }).then(
        (response) => {
          const result = _.sortBy(
            response.data.results.map((x) => ({
              value: x.id,
              text: x.label,
            })),
            'text'
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

<style scoped>
.auto_select {
  width: 18em !important;
}
</style>
