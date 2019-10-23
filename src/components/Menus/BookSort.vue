<template>
  <b-form-select
    id="sort-select"
    :value="value"
    @input="$emit('input', $event)"
    :options="sort_options"
  />
</template>

<script>
export default {
  name: "BookSort",
  props: {
    value: String
  },
  data() {
    return {
      sort_options: [
        { text: "Title A-Z", value: "pq_title" },
        { text: "Title Z-A", value: "-pq_title" },
        { text: "Author A-Z", value: "pq_author" },
        { text: "Author Z-A", value: "-pq_author" },
        { text: "Publisher A-Z", value: "pq_publisher" },
        { text: "Publisher Z-A", value: "-pq_publisher" },
        { text: "Oldest first", value: "date_early" },
        { text: "Recent first", value: "-date_early" }
      ]
    };
  }
};
</script>
