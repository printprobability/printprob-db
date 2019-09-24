<template>
  <div class="card">
    <div
      class="card-header d-flex justify-content-between align-items-center"
    >{{ spreads.length }} Spreads</div>
    <div class="card-body d-flex flex-wrap justify-content-between">
      <SpreadImage
        v-for="spread in spreads"
        :spread="spread"
        :key="spread.id"
        :header="String(spread.sequence)"
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
    spreads: Array
  }
};
</script>
