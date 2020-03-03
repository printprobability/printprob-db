<template>
  <a :href="line.image.web_url">
    <b-img-lazy
      :src="line.image.thumbnail"
      class="line-image my-3 mx-auto"
      @click="$emit('line_clicked', line)"
      blank-width="750"
      blank-height="200"
    />
  </a>
</template>

<script>
export default {
  name: "LineImage",
  props: {
    line: Object
  }
};
</script>

<style scoped>
img.line-image {
  max-width: 600px;
  max-height: 75px;
  border: 2px solid black;
}
</style>
