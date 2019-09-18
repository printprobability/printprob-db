<template>
  <div class="card">
    <div class="card-body"></div>
    <CharacterGroupingSelect />
    <CharacterGrouping :cg="selected_cg" />
  </div>
</template>

<script>
import CharacterGroupingSelect from "../Menus/CharacterGroupingSelect";
export default {
  name: "CharacterGroupingInterface",
  components: {
    CharacterGroupingSelect
  },
  data() {
    selected_cg: null;
  }
};
</script>