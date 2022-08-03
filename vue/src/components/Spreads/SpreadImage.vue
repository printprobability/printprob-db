<template>
  <div class="card spread-card my-2">
    <div class="card-header">
      <router-link v-if="link" :to="link">{{ header }}</router-link>
      <template v-else>{{ header }}</template>
    </div>
    <div class="card-body">
      <a :href="spread.image.web_url">
        <b-img-lazy
          class="spread-image"
          :src="spread.image.thumbnail"
          blank-width="500"
          blank-height="300"
        />
      </a>
    </div>
    <div v-if="footer" class="card-footer">{{ footer }}</div>
  </div>
</template>

<script>
export default {
  name: 'SpreadImage',
  props: {
    spread: Object,
    header: String,
    footer: String,
    link: {
      type: Object,
      default: null,
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.spread-image {
  max-width: 400px;
  max-height: 250px;
}
</style>
