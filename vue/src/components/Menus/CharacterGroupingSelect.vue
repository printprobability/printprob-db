<template>
  <div class="ui vertical segment">
    <div class="flexbox">
      <div class="flex-content">
        <b-form-group class="my-4">
          <model-select
            class="auto_select"
            v-if="all_groupings !== null"
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

// The grouping list is shared by every select on the page and kept in localStorage,
// so a menu shows the last known list at once while a fresh copy loads.
const CACHE_KEY = 'pp.character_groupings'
let cached = null

function readCache() {
  if (cached) return cached
  try {
    const stored = JSON.parse(window.localStorage.getItem(CACHE_KEY))
    if (Array.isArray(stored)) cached = stored
  } catch (e) {
    // no storage (private window etc.): wait for the request
  }
  return cached
}

function fetchGroupings() {
  return HTTP.get('/character_groupings/', { params: { limit: 500 } }).then(
    (response) => {
      cached = _.sortBy(
        response.data.results.map((x) => ({ value: x.id, text: x.label })),
        'text'
      )
      try {
        window.localStorage.setItem(CACHE_KEY, JSON.stringify(cached))
      } catch (e) {
        // storage full or blocked: the in-memory copy still works
      }
      return cached
    }
  )
}

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
      all_groupings: readCache(),
    }
  },
  computed: {
    character_groupings() {
      const result = this.all_groupings || []
      return this.excludedCharacterGroup
        ? result.filter(
            (option) => option.value !== this.excludedCharacterGroup
          )
        : result
    },
  },
  created() {
    fetchGroupings().then(
      (groupings) => {
        this.all_groupings = groupings
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
  width: 18em !important;
}
</style>
