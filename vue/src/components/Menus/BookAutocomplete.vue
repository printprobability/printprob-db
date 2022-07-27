<template>
  <Autocomplete
      :value="value"
      endpoint="/books/"
      :query_field="queryField"
      :label="label"
      description="Begin typing for suggestions"
      :displayLabel="displayLabel"
      n_choices="10"
      return_field="id"
      @input="fireInputEvent($event)"
      :additional_params="{ characters: true }"
  />
</template>

<script>
import Autocomplete from "./Autocomplete";

const BookSearchField = Object.freeze({
  pq_title: {
    query: 'pq_title',
    label: 'Source book by title',
  },
  printer_name: {
    query: 'printer_like',
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
  computed: {
    label() {
      return this.bookSearchField[this.field].label
    },
    queryField() {
      return this.bookSearchField[this.field].query
    },
  },
  methods: {
    displayLabel(book) {
      const bookTitle = book['pq_title']
      if (this.field === 'pq_title') {
        return this.addPrefixToLabel(book, bookTitle)
      }
      const printerName = book['pp_printer'] || book['colloq_printer']
      return this.addPrefixToLabel(book, `${printerName} - ${bookTitle}`)
    },
    fireInputEvent(bookId) {
      this.$emit('input', bookId)
    },
    addPrefixToLabel: function (book, displayLabel) {
      return `${this.prefix_field} ${book[this.prefix_field]}: ${displayLabel}`
    },
  },
  data: function () {
    return {
      bookSearchField: BookSearchField,
      prefix_field: 'vid'
    };
  },
};
</script>
