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
    <Spinner v-if="progress_spinner" />
    <table v-if="matched_characters.length">
      <thead>
        <tr>
          <th v-for="column in columnHeadings" :key="column">
            {{ column }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in matched_characters" :key="index">
          <td :key="row['target'].id">
            <CharacterImage :character="row['target']" image_size="bound100" />
          </td>
          <template v-for="match in row['matches']">
            <td :key="match.id">
              <CharacterImage :character="match" image_size="bound100" />
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import CharacterImage from '../Characters/CharacterImage'
import BookAutocomplete from '../Menus/BookAutocomplete'
import Spinner from '../Interfaces/Spinner'
import { HTTP } from '@/main'

export default {
  name: 'CharacterMatchesView',
  components: {
    CharacterImage,
    BookAutocomplete,
    Spinner,
  },
  data() {
    return {
      matched_directory: null,
      matched_character_class: null,
      matched_characters: [],
      match_directories: [],
      progress_spinner: false,
      directory_options: [],
      character_class_options: [],
      book: null,
      columnHeadings: [
        'Query',
        'Match1',
        'Match2',
        'Match3',
        'Match4',
        'Match5',
        'Match6',
        'Match7',
        'Match8',
        'Match9',
        'Match10',
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
  methods: {
    clear_book() {
      this.book = null
      this.progress_spinner = false
      this.directory_options = []
      this.matched_directory = null
      this.matched_character_class = null
      this.matched_characters = []
      this.match_directories = []
      this.progress_spinner = false
      this.directory_options = []
      this.character_class_options = []
    },
    book_selected(event) {
      this.book = event
      this.progress_spinner = true
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
    directory_selected(event) {
      this.matched_directory = event
      const character_classes = this.match_directories.first(
        (d) => (d.dir = this.matched_directory)
      ).character_classes
      this.character_class_options = character_classes.map(
        (character_class) => ({
          value: character_class,
          text: character_class,
        })
      )
    },
    character_class_selected(event) {
      this.matched_character_class = event
      this.progress_spinner = true
      HTTP.post('/books/' + this.book + '/matched_characters', {
        dir: this.matched_directory,
        character_class: this.matched_character_class,
      }).then(
        (response) => {
          this.matched_characters = response.data.matched_characters
          this.progress_spinner = false
        },
        (error) => {
          console.log(error)
          this.matched_characters = []
          this.progress_spinner = false
        }
      )
    },
  },
}
</script>

<style>
table {
  border: 2px solid black;
  border-radius: 3px;
  background-color: #fff;
}

td {
  background-color: #f9f9f9;
}

th {
  background-color: #42b983;
  color: rgba(255, 255, 255, 0.66);
  user-select: none;
}

th,
td {
  min-width: 120px;
  padding: 10px 20px;
}
</style>
