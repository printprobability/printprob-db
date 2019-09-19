<template>
  <div class="card">
    <div class="card-header">Create a new character group</div>
    <div class="card-body">
      <b-input v-model="label"></b-input>
      <b-input v-model="notes"></b-input>
      <b-button @click="create_new_group">Create</b-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "NewCharacterGrouping",
  data() {
    return {
      label: "",
      notes: ""
    };
  },
  methods: {
    create_new_group: function() {
      this.$emit("new_group", { label: this.label, notes: this.notes });
      this.label = "";
      this.notes = "";
    }
  }
};
</script>
