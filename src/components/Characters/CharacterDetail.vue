<template>
  <div class="container-flex" v-if="!!character">
    <h3>Character {{ character.label }}</h3>
    <AnnotatedImage :image_url="character.spread.image.web_url" :points="annotation" />
  </div>
</template>

<script>
import { HTTP } from "../../main";
import AnnotatedImage from "../Interfaces/AnnotatedImage";

export default {
  name: "CharacterDetail",
  components: {
    AnnotatedImage
  },
  props: {
    id: String
  },
  data() {
    return {
      character: null
    };
  },
  computed: {
    annotation() {
      return this.character.absolute_coords;
    }
  },
  methods: {
    get_character: function(id) {
      return HTTP.get("/characters/" + id + "/").then(
        response => {
          this.character = response.data;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted() {
    this.get_character(this.id);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
