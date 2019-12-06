<template>
  <div class="container-flex" v-if="!!spread">
    <h3>Spread {{ spread.label }}</h3>
    <AnnotatedImage :image_url="spread.image.web_url" :points="annotation" />
  </div>
</template>

<script>
import { HTTP } from "../../main";
import AnnotatedImage from "../Interfaces/AnnotatedImage";

export default {
  name: "SpreadDetail",
  components: {
    AnnotatedImage
  },
  props: {
    id: String
  },
  data() {
    return {
      spread: null,
      annotation: [
        { x: 20, y: 30 },
        { x: 350, y: 40 },
        { x: 340, y: 520 },
        { x: 50, y: 500 }
      ]
    };
  },
  methods: {
    get_spread: function(id) {
      return HTTP.get("/spreads/" + id + "/").then(
        response => {
          this.spread = response.data;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  created() {
    this.get_spread(this.id);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
