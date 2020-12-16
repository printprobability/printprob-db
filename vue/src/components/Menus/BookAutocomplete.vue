<template>
  <Autocomplete
    :value="value"
    endpoint="/books/"
    query_field="pq_title"
    label="Source book"
    description="Begin typing for suggestions"
    display_field="pq_title"
    n_choices="10"
    return_field="id"
    prefix_field="vid"
    @input="$emit('input', $event)"
    :additional_params="{ characters: true }"
  />
</template>

<script>
import Autocomplete from "./Autocomplete";

export default {
  name: "BookAutocomplete",
  components: {
    Autocomplete,
  },
  props: {
    value: {
      type: String,
      default: null,
    },
  },
};
</script>
