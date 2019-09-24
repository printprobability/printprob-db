<template>
  <div class="card my-2">
    <div class="card-header">
      <router-link v-if="link" :to="link">{{ header }}</router-link>
      <template v-else>{{ header }}</template>
    </div>
    <div class="card-body">
      <router-link :to="{name: 'PageDetailView', params: {id: page.id}}">
        <img class="page-image" :src="page.image.web_url" />
      </router-link>
    </div>
    <div v-if="footer" class="card-footer">{{ footer }}</div>
  </div>
</template>

<script>
export default {
  name: "PageImage",
  props: {
    page: Object,
    header: String,
    footer: String,
    link: {
      type: Object,
      default: null
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.page-image {
  width: 200px;
  max-height: 250px;
}
</style>
