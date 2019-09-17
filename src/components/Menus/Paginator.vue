<template>
  <div></div>
</template>

<script>
export default {
  name: "Paginator",
  props: {
    count: Number,
    next_page: String,
    prev_page: String
  },
  data() {
    currentPage: 1,

  }
};
</script>