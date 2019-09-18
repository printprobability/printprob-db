<template>
  <div class="card character-grouping">
    <div class="card-header">{{ cg.label }}</div>
    <div class="card-body">
      <p>
        <strong>Notes:</strong>
        {{ cg.notes }}
      </p>
    </div>
    <div class="card-footer">
      <small>Created by {{ cg.created_by }} on {{ display_date(cg.date_created) }}</small>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "CharacterGrouping",
  props: {
    cg: Object
  },
  data() {
    return {};
  },
  methods: {
    display_date: function(date) {
      return moment(new Date(date)).format("MM-DD-YY, h:mm a");
    }
  }
};
</script>