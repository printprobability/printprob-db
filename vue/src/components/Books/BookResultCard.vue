<template>
  <b-media>
    <template v-slot:aside>
      <div class="cover-image-frame">
        <b-img
          v-if="!!book.cover_spread"
          class="cover-image"
          :src="book.cover_spread.image.iiif_base +'/full/250,/0/default.jpg'"
          center
        />
        <small v-else>Not run yet</small>
      </div>
    </template>
    <router-link :to="{name: 'BookDetailView', params: {id: book.id}}">
      <h5>{{ truncate(book.pq_title, 140) }}</h5>
    </router-link>
    <b-row class="mt-3">
      <b-col cols sm="6" class="border-right">
        <p class="bg-light p-2">EEBO / ProQuest</p>
        <small>
          <a :href="book.pq_url">{{ book.pq_url }}</a>
        </small>
        <p>Author: {{ book.pq_author }}</p>
        <p>Publisher: {{ book.pq_publisher }}</p>
        <p>EEBO date: {{ book.pq_year_early }}-{{ book.pq_year_late }}</p>
        <p>TX A&M date: {{ book.tx_year_early }}-{{ book.tx_year_late }}</p>
        <p>
          EEBO ID:
          <code>{{ book.eebo }}</code>
        </p>
        <p>
          VID:
          <code>{{ book.vid }}</code>
        </p>
        <p>Spreads: {{ book.n_spreads }}</p>
        <p>
          Bridges zipfile:
          <code>{{ book.zipfile }}</code>
          <br />
          <code>unzip -d . {{ book.zipfile }}.zip {{ book.zipfile }}/{{ book.vid }}/*</code>
        </p>
      </b-col>
      <b-col cols sm="6">
        <p class="bg-light p-2">P&P</p>
        <b-button @click="set_star(!star_status)">star: {{ star_status }}</b-button>
        <p>Date between: {{ book.date_early }} and {{ book.date_late }}</p>
        <p>Publisher: {{ book.pp_publisher }}</p>
      </b-col>
    </b-row>
  </b-media>
</template>

<script>
import { HTTP } from "../../main";
export default {
  name: "BookResultCard",
  props: {
    book: Object
  },
  data() {
    return {
      star_status: false,
      ignored_status: false
    };
  },
  mounted() {
    this.star_status = this.book.starred;
    this.ignored_status = this.book.ignored;
  },
  computed: {
    object_url() {
      return "books/" + this.book.id + "/";
    }
  },
  methods: {
    truncate: function(input, length) {
      return input.length > length ? `${input.substring(0, length)}...` : input;
    },
    set_star(val) {
      HTTP.patch(this.object_url, { starred: val }).then(
        response => {
          this.star_status = response.data.starred;
        },
        error => {
          console.log(error);
        }
      );
    },
    set_ignore(val) {
      HTTP.patch(this.object_url, { ignored: val }).then(
        response => {
          this.ignored_status = response.data.ignored;
        },
        error => {
          console.log(error);
        }
      );
    }
  }
};
</script>

<style lang="css">
.cover-image-frame {
  width: 250px;
}

img.cover-image {
  max-width: 250px;
  max-height: 250px;
}
</style>
