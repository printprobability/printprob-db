<template>
  <b-media>
    <template v-slot:aside>
      <div class="cover-image-frame">
        <b-img-lazy
          v-if="!!book.cover_spread"
          class="cover-image"
          :src="book.cover_spread.image.iiif_base + '/full/250,/0/default.jpg'"
          center
        />
        <b-img-lazy
          v-else-if="!!book.cover_page"
          class="cover-image"
          :src="book.cover_page.image.iiif_base + '/full/250,/0/default.jpg'"
          center
        />
        <small v-else>Not run yet</small>
      </div>
    </template>
    <b-row align-v="center" align-h="between" class="pr-2">
      <router-link
        :to="{ name: 'BookDetailView', params: { id: book.id } }"
        target="_blank"
        rel="noopener noreferrer"
      >
        <h5>{{ truncate(book.pq_title, 140) }}</h5>
      </router-link>
      <button class="star_button" @click="set_star(!star_status)">
        <font-awesome-icon :icon="star_icon" />
      </button>
    </b-row>
    <b-row class="mt-3">
      <b-col cols sm="6" class="border-right">
        <p class="bg-light p-2">EEBO / ProQuest</p>
        <small>
          <a :href="book.pq_url">{{ book.pq_url }}</a>
        </small>
        <p>Author: {{ book.pq_author }}</p>
        <p>Publisher: {{ book.pq_publisher }}</p>
        <p>EEBO date: {{ book.pq_year_early }}-{{ book.pq_year_late }}</p>
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
          Bridges images:
          <code
            >/pylon5/hm4s82p/shared/eebo_unzipped/{{ book.zipfile }}/{{
              book.vid
            }}/</code
          >
        </p>
      </b-col>
      <b-col cols sm="6">
        <p class="bg-light p-2">P&P</p>
        <p>Date between: {{ book.date_early }} and {{ book.date_late }}</p>
        <p>Publisher: {{ book.pp_publisher }}</p>
        <p>Repository: {{ book.repository }}</p>
      </b-col>
    </b-row>
  </b-media>
</template>

<script>
import { HTTP } from "../../main";
export default {
  name: "BookResultCard",
  props: {
    book: Object,
  },
  data() {
    return {
      star_status: false,
      ignored_status: false,
    };
  },
  mounted() {
    this.star_status = this.book.starred;
    this.ignored_status = this.book.ignored;
  },
  computed: {
    object_url() {
      return "books/" + this.book.id + "/";
    },
    star_icon() {
      if (this.star_status) {
        return ["fas", "star"];
      } else {
        return ["far", "star"];
      }
    },
  },
  methods: {
    truncate: function (input, length) {
      return input.length > length ? `${input.substring(0, length)}...` : input;
    },
    set_star(val) {
      HTTP.patch(this.object_url, { starred: val }).then(
        (response) => {
          this.star_status = response.data.starred;
        },
        (error) => {
          console.log(error);
        }
      );
    },
    set_ignore(val) {
      HTTP.patch(this.object_url, { ignored: val }).then(
        (response) => {
          this.ignored_status = response.data.ignored;
        },
        (error) => {
          console.log(error);
        }
      );
    },
  },
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

button.star_button {
  padding: 0;
  border: none;
  background: none;
  font-size: 1.25rem;
  color: goldenrod;
}
</style>
