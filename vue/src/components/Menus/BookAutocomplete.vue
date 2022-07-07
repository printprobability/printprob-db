<template>
  <Autocomplete
    :value="value"
    endpoint="/books/"
    :query_field="bookSearchField[field].query"
    :label="bookSearchField[field].label"
    description="Begin typing for suggestions"
    :display_field="bookSearchField[field].displayField"
    n_choices="10"
    return_field="id"
    prefix_field="vid"
    @input="$emit('input', $event)"
    :additional_params="{ characters: true }"
  />
</template>

<script>
import Autocomplete from "./Autocomplete";

const BookSearchField = Object.freeze({
  pq_title: {
    query: 'pq_title',
    displayField: 'pq_title',
    label: 'Source book by title',
  },
  printer_name: {
    query: 'printer_like',
    displayField: 'printer_like',
    label: 'Source book by printer name',
  }
})

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
    field: {
      type: String,
      default: null,
    },
  },
  data: function() {
    return {
      bookSearchField: BookSearchField
    };
  },};
</script>
