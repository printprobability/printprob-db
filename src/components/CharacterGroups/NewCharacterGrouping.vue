<template>
  <div class="card">
    <div class="card-header">
      Create a new character group
      <b-button @click="$emit('cancel_create')" size="sm" variant="warning">X</b-button>
    </div>
    <div class="card-body">
      <b-input v-model="label" placeholder="Label (required)" :state="label_state"></b-input>
      <b-input v-model="notes" placeholder="Notes"></b-input>
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
  computed: {
    label_state: function() {
      return this.label.length > 1;
    }
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
