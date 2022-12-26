<template>
  <div class="container-fluid">
    <h1 class="my-2">Review Character Matches</h1>
    <div class="card">
      <div class="card-header">Select Book</div>
      <div class="card-body">
        <div class="row">
          <div class="col-4">
            <p v-if="!!book">
              <b-button @click="clear_book" variant="danger" size="sm"
                >x
              </b-button>
              <strong>Book:</strong>
              {{ book_title }}
            </p>
            <div v-else>
              <BookAutocomplete :value="book" @input="book_selected" />
            </div>
          </div>
          <div class="col-2" v-if="!!book">
            <b-form-select
              id="matched-directory"
              :value="matched_directory"
              @input="directory_selected"
              :options="directory_options"
            />
          </div>
          <div class="col-2" v-if="!!matched_directory">
            <b-form-select
              id="matched-character-class"
              :value="matched_character_class"
              @input="character_class_selected"
              :options="character_class_options"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="!!matched_character_class">
      <b-table
        responsive
        sticky-header="70vh"
        :fields="fields"
        :items="items"
        :busy="progress_spinner"
        head-variant="light"
        :no-border-collapse="true"
      >
        <template #head(name)="data">
          <span class="text-info">{{ data.label.toUpperCase() }}</span>
        </template>
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
        <template #cell(query)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="0"
            :character_row="data.value"
          />
        </template>
        <template #cell(match1)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="1"
            :character_row="data.value"
          />
        </template>
        <template #cell(match2)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="2"
            :character_row="data.value"
          />
        </template>
        <template #cell(match3)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="3"
            :character_row="data.value"
          />
        </template>
        <template #cell(match4)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="4"
            :character_row="data.value"
          />
        </template>
        <template #cell(match5)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="5"
            :character_row="data.value"
          />
        </template>
        <template #cell(match6)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="6"
            :character_row="data.value"
          />
        </template>
        <template #cell(match7)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="7"
            :character_row="data.value"
          />
        </template>
        <template #cell(match8)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="8"
            :character_row="data.value"
          />
        </template>
        <template #cell(match9)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="9"
            :character_row="data.value"
          />
        </template>
        <template #cell(match10)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="10"
            :character_row="data.value"
          />
        </template>
      </b-table>
      <b-pagination
        v-model="page"
        :total-rows="total_count"
        :per-page="per_page"
        first-text="First"
        prev-text="Prev"
        next-text="Next"
        last-text="Last"
        @change="on_page_change"
      />
    </div>
  </div>
</template>

<script>
import CharacterMatchImage from '../Characters/CharacterMatchImage'
import BookAutocomplete from '../Menus/BookAutocomplete'
import { HTTP } from '@/main'

export default {
  name: 'CharacterMatchesView',
  components: {
    CharacterMatchImage,
    BookAutocomplete,
  },
  data() {
    return {
      matched_directory: null,
      matched_character_class: null,
      match_directories: [],
      progress_spinner: false,
      directory_options: [],
      character_class_options: [],
      book: null,
      items: [],
      total_count: 0,
      per_page: 10,
      page: 1,
      fields: [
        'query',
        'match1',
        'match2',
        'match3',
        'match4',
        'match5',
        'match6',
        'match7',
        'match8',
        'match9',
        'match10',
      ],
    }
  },
  asyncComputed: {
    book_title() {
      if (!!this.book) {
        return HTTP.get('/books/' + this.book + '/').then(
          (response) => {
            return response.data.label
          },
          (error) => {
            console.log(error)
          }
        )
      }
    },
  },
  created() {
    this.book = this.$route.query.book
    if (this.book) {
      this.update_directories()
    }
  },
  updated() {
    this.$router.push({
      name: 'CharacterMatchesView',
      query: this.view_params,
    })
  },
  computed: {
    view_params() {
      return {
        book: this.book,
      }
    },
  },
  methods: {
    on_page_change() {
      this.fetch_characters()
    },
    clear_book() {
      this.book = null
      this.progress_spinner = false
      this.directory_options = []
      this.matched_directory = null
      this.matched_character_class = null
      this.match_directories = []
      this.progress_spinner = false
      this.directory_options = []
      this.character_class_options = []
    },
    update_directories() {
      HTTP.get('/books/' + this.book + '/matched_directories').then(
        (response) => {
          this.match_directories = response.data.match_directories
          this.directory_options = this.match_directories.map((d) => ({
            value: d.dir,
            text: d.dir,
          }))
          this.directory_options = [
            { value: null, text: 'Please select a directory' },
          ].concat(this.directory_options)
          this.progress_spinner = false
        },
        (error) => {
          console.log(error)
          this.directory_options = []
          this.progress_spinner = false
        }
      )
    },
    book_selected(event) {
      if (event == null) {
        return
      }
      this.book = event
      this.progress_spinner = true
      this.update_directories()
    },
    directory_selected(event) {
      if (event == null) {
        return
      }
      this.matched_directory = event
      this.matched_character_class = null
      this.items = []
      const character_classes = this.match_directories.find(
        (d) => (d.dir = this.matched_directory)
      ).character_classes
      this.character_class_options = character_classes.map(
        (character_class) => ({
          value: character_class,
          text: character_class,
        })
      )
      this.character_class_options = [
        { value: null, text: 'Please select a character class' },
      ].concat(this.character_class_options)
    },
    format_response_for_table(matched_characters) {
      const formatted_items = []
      for (const matched_character of matched_characters) {
        const item = {
          query: matched_character['target'],
        }
        for (let i = 0; i < matched_character['matches'].length; i++) {
          item[`match${i + 1}`] = matched_character['matches'][i]
        }
        formatted_items.push(item)
      }
      this.items = formatted_items
    },
    character_class_selected(event) {
      if (event == null) {
        return
      }
      this.matched_character_class = event
      this.fetch_characters()
    },
    fetch_characters() {
      const offset = (this.page - 1) * this.per_page + 1
      this.progress_spinner = true
      HTTP.post(
        '/books/' +
          this.book +
          `/matched_characters/?offset=${offset}&limit=${this.per_page}`,
        {
          dir: this.matched_directory,
          character_class: this.matched_character_class,
        }
      ).then(
        (response) => {
          this.format_response_for_table(response.data.matched_characters)
          this.total_count = response.data.total_count
          this.progress_spinner = false
        },
        (error) => {
          console.log(error)
          this.items = []
          this.progress_spinner = false
        }
      )
    },
  },
}
</script>
