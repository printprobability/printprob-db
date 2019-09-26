<template>
  <div class="container-fluid">
    <h1>Review character quality</h1>
    <CharacterList @update="update_displayed_images" @char_clicked="strike_character" />
    <b-button block @click="mark_good" variant="success">Mark remaining characters as good</b-button>
  </div>
</template>

<script>
import CharacterList from "../Characters/CharacterList";

export default {
  name: "CharacterReviewInterface",
  components: {
    CharacterList
  },
  data() {
    return {
      displayed_images: []
    };
  },
  methods: {
    update_displayed_images: function(imgs) {
      this.displayed_images = imgs;
    },
    strike_character: function() {
      return null;
    }
  }
};
</script>
