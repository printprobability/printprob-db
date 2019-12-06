<template>
  <div class="container-fluid">
    <h2>Spreads</h2>
    <div class="d-flex justify-content-left flex-wrap">
      <SpreadImage
        class="m-2"
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
