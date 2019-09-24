<template>
  <div class="container">
    <b-form-group id="label-group" label="Label" description="Required">
      <b-input id="notes-input" v-model="label" placeholder="Label (required)" :state="label_state"></b-input>
    </b-form-group>
    <b-form-group id="notes-group" label="Notes">
      <b-input id="notes-input" v-model="notes" placeholder="Notes"></b-input>
    </b-form-group>
    <b-button @click="create_new_group" variant="success">Create</b-button>
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
