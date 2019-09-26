<template>
  <img :src="line.image.web_url" class="line-image my-3 mx-auto" @click="$emit('line.click', line)" />
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
  max-width: 800px;
  max-height: 200px;
  border: 2px solid black;
}
</style>
