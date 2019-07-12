<template>
  <div class="card m-2">
    <div class="card-header">{{ page.sequence }} - {{ page.side }}</div>
    <div class="card-body">
      <router-link :to="{name: 'PageDetailView', params: {id: page.pk}}">
        <img class="page-image" :src="page.pref_image.web_url">
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "PageImage",
  props: {
    page: Object
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
