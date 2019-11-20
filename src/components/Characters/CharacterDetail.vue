<template>
  <div class="container-flex" v-if="!!character">
    <h3>Character {{ character.label }}</h3>
    <AnnotatedImage :id="this.character.id" :image_info_url="image_info_url" />
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
    },
    image_info_url() {
      return this.character.page.image.iiif_base + "/info.json";
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
