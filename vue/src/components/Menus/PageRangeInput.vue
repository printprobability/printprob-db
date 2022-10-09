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
    page_range: {
      type: Array,
      default() {
        return []
      },
    },
  },
  data() {
    return {
      gte: this.page_range[0],
      lte: this.page_range[1],
    }
  },
  methods: {
    renderRange() {
      if (this.gte) {
        this.$emit('input', [this.gte, this.lte])
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
