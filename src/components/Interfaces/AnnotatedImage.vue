<template>
  <div :id="id" class="osd"></div>
</template>

<script>
import OpenSeadragon from "openseadragon";

export default {
  name: "AnnotatedImage",
  props: {
    id: String,
    image_info_url: String
  },
  data() {
    return {};
  },
  computed: {
    options() {
      return {
        id: this.id,
        prefixUrl: "/osd/",
        tileSources: this.image_info_url,
        maxZoomLevel: 3
      };
    }
  },
  mounted() {
    OpenSeadragon(this.options);
  },
  updated() {
    OpenSeadragon(this.options);
  }
};
</script>

<style scoped>
.osd {
  height: 1000px;
  width: 100%;
}
</style>
