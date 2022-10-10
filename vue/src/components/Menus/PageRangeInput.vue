<template>
  <b-form-group id="page-range-group" label="Page range" label-size="sm">
    <b-form inline>
      <b-input size="sm" id="gte" v-model="gte" />
      to
      <b-input size="sm" id="lte" v-model="lte" />
    </b-form>
  </b-form-group>
</template>

<script>
export default {
  name: 'PageRangeInput',
  props: {
    page_start: {
      type: Number,
      default: null,
    },
    page_end: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      gte: this.page_start,
      lte: this.page_end,
    }
  },
  methods: {
    renderRange() {
      if (this.gte) {
        if (this.lte) {
          if (this.gte <= this.lte) {
            this.$emit('input', [this.gte, this.lte])
          }
        } else {
          this.$emit('input', [this.gte, this.lte])
        }
      } else {
        this.$emit('input', [null, null])
      }
    },
  },
  watch: {
    gte(newVal, prevVal) {
      if (newVal !== prevVal) {
        this.renderRange()
      }
    },
    lte(newVal, prevVal) {
      if (newVal !== prevVal) {
        this.renderRange()
      }
    },
  },
}
</script>
