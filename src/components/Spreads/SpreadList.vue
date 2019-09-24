<template>
  <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
      {{ book.spreads.length }} Spreads
      <b-button variant="success" :href="book.pdf">Download PDF</b-button>
    </div>
    <div class="card-body d-flex flex-wrap justify-content-between">
      <SpreadImage
        v-for="spread in book.spreads"
        :spread="spread"
        :key="spread.id"
        :header="spread.sequence"
      />
    </div>
  </div>
</template>

<script>
import SpreadImage from "../Spreads/SpreadImage";

export default {
  name: "SpreadList",
  components: {
    SpreadImage
  },
  props: {
    book: Object
  }
};
</script>