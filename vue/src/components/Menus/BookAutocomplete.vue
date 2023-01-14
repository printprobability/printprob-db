<template>
  <div>
    <b-form-group
      label="Source book by:"
      label-cols-sm="3"
      label-align-sm="left"
      label-size="md"
      class="mb-0"
      v-slot="{ ariaDescribedby }"
    >
      <b-form-radio-group
        class="pt-2"
        v-model="source_type"
        size="md"
        :aria-describedby="ariaDescribedby"
      >
        <b-form-radio value="title">Book Title</b-form-radio>
        <b-form-radio value="printer">Printer Name</b-form-radio>
      </b-form-radio-group>
    </b-form-group>
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
  </div>
</template>

<script>
import Autocomplete from './Autocomplete'

const BookSearchField = Object.freeze({
  title: {
    query: 'pq_title',
    label: 'Source book by title',
  },
  printer: {
    query: 'printer_like',
    label: 'Source book by printer name',
  },
})

export default {
  name: 'BookAutocomplete',
  components: {
    Autocomplete,
  },
  props: {
    value: {
      type: String,
      default: null,
    },
  },
  computed: {
    label() {
      return this.bookSearchField[this.source_type].label
    },
    queryField() {
      return this.bookSearchField[this.source_type].query
    },
  },
  methods: {
    displayLabel(book) {
      const estcNumber = book['estc']
      const date = book['pq_year_early'] || book['tx_year_early']
      const bookTitle =
        (estcNumber ? `ESTC: ${estcNumber} - ` : '') +
        (date ? `Published: ${date} - ` : '') +
        book['pq_title']
      if (this.source_type === 'title') {
        return this.addPrefixToLabel(book, bookTitle)
      }
      const printerName = book['pp_printer'] || book['colloq_printer']
      return this.addPrefixToLabel(book, `${printerName} - ${bookTitle}`)
    },
    fireInputEvent(bookId) {
      this.$emit('input', bookId)
    },
    addPrefixToLabel: function (book, displayLabel) {
      return `${this.prefix_field} ${book[this.prefix_field]} - ${displayLabel}`
    },
  },
  data: function () {
    return {
      bookSearchField: BookSearchField,
      prefix_field: 'vid',
      source_type: 'title',
    }
  },
}
</script>
