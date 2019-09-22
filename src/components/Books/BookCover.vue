<template>
  <div class="card book-card m-2">
    <div class="card-header">
      <router-link :to="{name: 'BookDetailView', params: {id: book.eebo}}">{{ book.title }}</router-link>
      ({{ book.n_spreads }} spreads)
    </div>
    <div class="card-body">
      <img :src="book.cover_page.image.web_url" class="book-cover-image" />
    </div>
    <div class="card-footer">
      <p>
        EEBO id:
        <code>{{ book.eebo }}</code>
      </p>
      <p></p>
    </div>
  </div>
</template>

<script>
export default {
  name: "BookCover",
  props: {
    book: Object
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.book-cover-image {
  max-width: 200px;
  max-height: 250px;
}

div.card-footer code {
  font-size: 60%;
}
</style>
