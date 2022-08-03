<template>
  <div :id="id" class="osd"></div>
</template>

<script>
import { HTTP } from '../../main'
import OpenSeadragon from 'openseadragon'

export default {
  name: 'AnnotatedImage',
  props: {
    id: String,
    image_info_url: String,
    overlay: Object,
  },
  data() {
    return {
      image_info_data: null,
    }
  },
  computed: {
    options() {
      return {
        id: this.id,
        prefixUrl: '/osd/',
        tileSources: [this.image_info_data],
        maxZoomLevel: 3,
        overlays: this.overlays,
      }
    },
    overlays() {
      return [
        {
          id: 'overlay' + this.id,
          px: this.overlay.x,
          py: this.overlay.y,
          width: this.overlay.w,
          height: this.overlay.h,
          className: 'overlay',
        },
      ]
    },
  },
  mounted() {
    HTTP.get(this.image_info_url).then(
      (response) => {
        var res = response.data
        res['@id'] = res['@id'].replace(
          /http.+8080/,
          'https://printprobdb.psc.edu/iiif'
        )
        this.image_info_data = res
        OpenSeadragon(this.options)
      },
      (error) => {
        console.log(error)
      }
    )
  },
  updated() {
    OpenSeadragon(this.options)
  },
}
</script>

<style>
.osd {
  height: 750px;
  min-width: 100%;
}

.overlay {
  outline: red 5px solid;
}
</style>
