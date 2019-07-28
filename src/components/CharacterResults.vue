<template>
  <div class="d-flex flex-wrap char-images">
    <CharacterImage v-for="character in characters" :character="character" :key="character.id" />
  </div>
</template>

<script>
import CharacterImage from "./CharacterImage.vue";
export default {
  name: "CharacterResults",
  props: {
    selected_character_class: String
  },
  components: {
    CharacterImage
  },
  data: function(d) {
    return {
      characters: []
    };
  },
  methods: {
    get_characters: function(l = "http://localhost/characters/") {
      console.log(this.selected_character_class);
      // if (!!cname) {
      //   var param_payload = { character_class: cname };
      // } else {
      //   var param_payload = null;
      // }
      if (!!this.selected_character_class) {
        console.log(this.selected_character_class);
        return this.$http
          .get(l, {
            params: { character_class: this.selected_character_class }
          })
          .then(
            response => {
              // // Page through results recursively
              // if (!!response.data.next) {
              //   console.log(response.data.next);
              //   var payload =
              //     response.data.results + get_characters(response.data.next);
              // } else {
              //   var payload = response.data.results;
              // }
              this.characters = response.data.results;
            },
            error => {
              console.log(error);
            }
          );
      } else {
        console.log(l);
        return this.$http.get(l).then(
          response => {
            this.characters = response.data.results;
          },
          error => {
            console.log(error);
          }
        );
      }
    }
  },
  mounted: function() {
    this.get_characters();
  }
};
</script>

<style>
</style>
