<template>
  <img
    :src="character.image.web_url"
    class="character-image my-1 mx-auto"
    v-b-tooltip.hover
    :title="character_tooltip"
  />
</template>

<script>
export default {
  name: 'NextPage',
  props: {
    path: String,
  },
}
</script>

<style></style>
