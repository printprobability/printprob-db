<template>
  <v-stage :config="config_konva" ref="stage">
    <v-layer ref="layer">
      <v-image :config="{image: image}"></v-image>
      <v-line :config="annotation" id="annotation_box" />
    </v-layer>
  </v-stage>
</template>

<script>
export default {
  name: "AnnotatedImage",
  props: {
    image_url: String,
    points: Array
  },
  data() {
    return {
      image: null,
      config_konva: { width: 0, height: 0 }
    };
  },
  computed: {
    annotation() {
      return {
        points: this.points
          .map(p => {
            return [p.x, p.y];
          })
          .flat(),
        closed: true,
        stroke: "red",
        strokeWidth: 4
      };
    }
  },
  methods: {
    get_image: function(url) {
      const image = new window.Image();
      image.src = url;
      image.onload = () => {
        // set image only when it is loaded
        this.config_konva.height = image.height;
        this.config_konva.width = image.width;
        this.image = image;
      };
    }
  },
  created() {
    this.get_image(this.image_url);
  }
};
</script>
