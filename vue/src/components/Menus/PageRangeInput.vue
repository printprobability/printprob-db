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
  name: "PageRangeInput",
  props: {
    page_range: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      gte: null,
      lte: null,
    };
  },
  methods: {
    renderRange() {
      this.$emit("input", [this.gte, this.lte]);
    },
  },
  watch: {
    gte() {
      this.renderRange();
    },
    lte() {
      this.renderRange();
    },
  },
  created() {
    this.gte = this.page_range[0];
    this.lte = this.page_range[1];
  },
};
</script>
