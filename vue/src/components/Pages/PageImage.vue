<template>
  <div class="card m-2">
    <div class="card-header">
      <router-link v-if="link" :to="link">{{ header }}</router-link>
      <template v-else>{{ header }}</template>
    </div>
    <div class="card-body">
      <a :href="page.image.web_url">
        <b-img-lazy
          class="page-image"
          :src="page.image.thumbnail"
          blank-width="300"
          blank-height="500"
        />
      </a>
    </div>
    <div v-if="footer" class="card-footer">{{ footer }}</div>
  </div>
</template>

<script>
export default {
  name: 'PageImage',
  props: {
    page: Object,
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
img.page-image {
  max-width: 200px;
  max-height: 250px;
}
</style>
