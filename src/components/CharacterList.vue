<template>
  <div id="app">
    <b-form-select
      v-model="selected_character_class"
      :options="character_classes"
      @input="input_charclass"
    ></b-form-select>
    <CharacterResults
      :selected_character_class="this.$route.query.classname"
      :key="this.$route.query.classname"
    />
  </div>
</template>

<script>
import CharacterResults from "./CharacterResults.vue";

export default {
  name: "CharacterList",
  components: {
    CharacterResults
  },
  data: function(d) {
    return {
      character_classes: [],
      selected_character_class: null
    };
  },
  methods: {
    input_charclass: function() {
      this.$router.push({
        name: "CharacterListView",
        query: { classname: this.selected_character_class }
      });
    },
    get_charcacter_classes: function(
      l = "http://localhost/character_classes/"
    ) {
      return this.$http.get(l).then(
        response => {
          var classnames = response.data.results.map(x => x.classname);
          this.character_classes = classnames;
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  mounted: function() {
    this.get_charcacter_classes();
  }
};
</script>

<style>
</style>
