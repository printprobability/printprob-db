<template>
  <div id="app">
    <b-form-select
      v-model="selected_character_class"
      :state="this.$route.query.classname"
      :options="character_classes"
      @input="input_charclass"
    ></b-form-select>
    <CharacterResults :selected_character_class="this.$route.query.classname" />
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
          // Page through results recursively
          if (!!response.data.next) {
            console.log(response.data.next);
            var payload =
              response.data.results +
              get_charcacter_classes(response.data.next);
          } else {
            var payload = response.data.results;
          }
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
