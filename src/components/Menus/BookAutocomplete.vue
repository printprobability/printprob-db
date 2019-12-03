<template>
  <Autocomplete
    :value="value"
    endpoint="/books/"
    query_field="pq_title"
    label="Source book"
    description="Begin typing for suggestions"
    placeholder="an answer to nine"
    display_field="label"
    n_choices="10"
    return_field="id"
    @input="$emit('input', $event)"
  />
</template>

<script>
import Autocomplete from "./Autocomplete";

export default {
  name: "BookAutocomplete",
  components: {
    Autocomplete
  },
  props: {
    value: {
      type: String,
      default: null
    }
  }
};
</script>
