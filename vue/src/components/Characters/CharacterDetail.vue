<template>
  <b-row v-if="!!character">
    <b-col cols="3">
      <b-card header="Character detail" class="m-2">
        <p>
          Book:
          <router-link
            :to="{
              name: 'BookDetailView',
              params: { id: this.character.book.id },
            }"
            >{{ this.character.book.label }}</router-link
          >
        </p>
        <p>
          Location: page {{ this.character.page.sequence }}, line
          {{ this.character.line.sequence }}, position
          {{ this.character.sequence }}
        </p>
        <p>
          Assigned class: {{ this.character.character_class }} ({{
            this.character.class_probability
          }})
        </p>
        <p>Human character class: {{ this.character.human_character_class }}</p>
        <p>
          Character id:
          <code>{{ this.character.id }}</code>
        </p>
      </b-card>
    </b-col>
    <b-col cols="9">
      <div class="m-2">
        <AnnotatedImage
          :id="this.character.id"
          :image_info_url="image_info_url"
          :overlay="annotation"
        />
      </div>
    </b-col>
  </b-row>
</template>

<script>
import { HTTP } from "../../main";
import AnnotatedImage from "../Interfaces/AnnotatedImage";

export default {
  name: "CharacterDetail",
  components: {
    AnnotatedImage,
  },
  props: {
    id: String,
  },
  data() {
    return {};
  },
  asyncComputed: {
    character() {
      return HTTP.get("/characters/" + this.id + "/").then(
        (response) => {
          return response.data;
        },
        (error) => {
          console.log(error);
        }
      );
    },
  },
  computed: {
    annotation() {
      return this.character.absolute_coords;
    },
    image_info_url() {
      return this.character.page.image.iiif_base + "/info.json";
    },
  },
};
</script>
