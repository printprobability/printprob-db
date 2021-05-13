<template>
  <div :id="id" class="osd"></div>
</template>

<script>
import { HTTP } from "../../main";
import OpenSeadragon from "openseadragon";

export default {
  name: "AnnotatedImage",
  props: {
    id: String,
    image_info_url: String,
    overlay: Object,
  },
  data() {
    return {};
  },
  computed: {
    rewritten_image_info() {
      return HTTP.get(this.image_info_url).then(
        (response) => {
          var res = response.data;
          res["@id"] = res["@id"].replace(
            /http.+8080/,
            `${$APIConstants.PP_HOST}/iiif`
          );
          return res;
        },
        (error) => {
          console.log(error);
        }
      );
    },
    options() {
      return {
        id: this.id,
        prefixUrl: "/osd/",
        tileSources: this.rewritten_image_info,
        maxZoomLevel: 3,
        overlays: this.overlays,
      };
    },
    overlays() {
      return [
        {
          id: "overlay" + this.id,
          px: this.overlay.x,
          py: this.overlay.y,
          width: this.overlay.w,
          height: this.overlay.h,
          className: "overlay",
        },
      ];
    },
  },
  mounted() {
    OpenSeadragon(this.options);
  },
  updated() {
    OpenSeadragon(this.options);
  },
};
</script>

<style>
.osd {
  height: 750px;
  width: 100%;
}

.overlay {
  outline: red 5px solid;
}
</style>
