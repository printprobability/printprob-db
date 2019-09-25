<template>
  <div class="card-columns">
    <SpreadImage
      v-for="spread in spreads"
      :spread="spread"
      :key="spread.id"
      :header="String(spread.sequence)"
    />
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
