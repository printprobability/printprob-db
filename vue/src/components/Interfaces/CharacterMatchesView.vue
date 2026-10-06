<template>
  <div class="container-fluid">
    <h1 class="my-2">Review Character Matches</h1>
    <div class="card">
      <div class="card-header">Select Book</div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-5">
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
          <div class="col-md-2" v-if="!!matched_directory">
            <b-form-select
              id="matched-character-class"
              :value="matched_character_class"
              @input="character_class_selected"
              :options="character_class_options"
            />
          </div>
          <div class="col-md-5" v-if="items.length > 0">
            <b-form-group label="Image size" label-cols="auto">
              <b-form-radio-group
                v-model="image_size"
                name="image-size"
                :options="image_size_options"
              />
            </b-form-group>
          </div>
        </div>
        <div class="row mt-2" v-if="!!book">
          <div class="col-md-3">
            <b-form-input
              v-model="directory_filter"
              placeholder="Filter runs, e.g. locke, 457, auto"
              debounce="200"
            />
          </div>
          <div class="col-md-9">
            <b-form-select
              id="matched-directory"
              :value="matched_directory"
              @input="directory_selected"
              :options="directory_options"
            />
          </div>
        </div>
      </div>
    </div>
    <b-card
      v-if="!!matched_directory"
      class="my-2"
      header="Now viewing"
      header-class="py-1"
      body-class="py-2"
    >
      <dl class="row mb-0 small">
        <template v-for="line in run_details">
          <dt class="col-sm-2" :key="line.label + '-label'">
            {{ line.label }}
          </dt>
          <dd class="col-sm-10" :key="line.label + '-text'">
            {{ line.text }}
          </dd>
        </template>
        <template v-if="!!matched_character_class">
          <dt class="col-sm-2">Letter</dt>
          <dd class="col-sm-10">
            {{ matched_character_class }}: {{ total_count }} queries (page
            {{ page }} of {{ num_pages }}), each shown with its nearest
            candidates by rank; lower distance means closer. Distances are
            rounded to 2 decimals, so very close candidates can all show 0.
            Click candidates to tick them, then "Declare match…" to add them to
            a character grouping.
          </dd>
        </template>
        <dt class="col-sm-2">Folder</dt>
        <dd class="col-sm-10">
          <code>{{ matched_directory }}</code>
          <b-button size="sm" variant="link" class="py-0" @click="copy_dir"
            >copy</b-button
          >
        </dd>
      </dl>
    </b-card>
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
            :image_size="image_size"
          />
          <b-button
            size="sm"
            variant="outline-primary"
            class="mt-1"
            :disabled="
              !selected_matches[data.index] ||
              selected_matches[data.index].size === 0
            "
            @click="open_declare(data.index)"
            >Declare match…</b-button
          >
          <b-badge
            v-if="data.value && declared[data.value.id]"
            variant="success"
            class="d-block mt-1 text-wrap"
            >declared → {{ declared[data.value.id] }}</b-badge
          >
        </template>
        <template #cell(match1)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="1"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match2)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="2"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match3)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="3"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match4)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="4"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match5)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="5"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match6)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="6"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match7)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="7"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match8)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="8"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match9)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="9"
            :character_row="data.value"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match10)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="10"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match11)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="11"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match12)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="12"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match13)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="13"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match14)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="14"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match15)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="15"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match16)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="16"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match17)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="17"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match18)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="18"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match19)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="19"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
          />
        </template>
        <template #cell(match20)="data">
          <CharacterMatchImage
            :index="data.index + 1"
            col_index="20"
            :character_row="data.value"
            @char_clicked="char_selected($event)"
            :selected="selected_matches"
            is_match_image
            :image_size="image_size"
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
    <b-modal
      v-model="declare.show"
      title="Declare match"
      size="lg"
      ok-title="Declare"
      :ok-disabled="!declare_ready || declare.busy"
      @ok.prevent="submit_declare"
    >
      <p class="small mb-1"><strong>Query:</strong> {{ declare.query_text }}</p>
      <p class="small mb-1">
        <strong>Matched ({{ declare.matches.length }}):</strong>
      </p>
      <ul class="small">
        <li v-for="m in declare.matches" :key="m.id">{{ m.text }}</li>
      </ul>
      <b-form-checkbox v-model="declare.new_group" class="mb-2">
        Create a new group for this match instead
      </b-form-checkbox>
      <div v-if="!declare.new_group">
        <CharacterGroupingSelect
          v-model="declare.group_id"
          label="Add to an existing group…"
        />
      </div>
      <div v-else>
        <b-form-group label="New group label" label-size="sm">
          <b-form-input v-model="declare.label" size="sm" maxlength="200" />
        </b-form-group>
        <b-form-group label="Group notes (optional)" label-size="sm">
          <b-form-textarea v-model="declare.notes" size="sm" rows="2" />
        </b-form-group>
      </div>
      <b-form-group
        label="Provenance (appended to the group's notes)"
        label-size="sm"
      >
        <b-form-textarea v-model="declare.provenance" size="sm" rows="3" />
      </b-form-group>
      <b-alert :show="!!declare.error" variant="danger" class="small">
        {{ declare.error }}
      </b-alert>
    </b-modal>
  </div>
</template>

<script>
import CharacterMatchImage from '../Characters/CharacterMatchImage'
import BookAutocomplete from '../Menus/BookAutocomplete'
import CharacterGroupingSelect from '../Menus/CharacterGroupingSelect'
import { HTTP } from '@/main'
import {
  parseMatchDir,
  describeRunShort,
  describeRunLong,
  characterCaption,
} from '@/utils/matchRuns'

function emptyDeclare() {
  return {
    show: false,
    busy: false,
    error: '',
    query_id: null,
    query_text: '',
    matches: [],
    new_group: false,
    group_id: null,
    label: '',
    notes: '',
    provenance: '',
  }
}

export default {
  name: 'CharacterMatchesView',
  components: {
    CharacterMatchImage,
    BookAutocomplete,
    CharacterGroupingSelect,
  },
  data() {
    return {
      matched_directory: null,
      matched_character_class: null,
      match_directories: [],
      progress_spinner: false,
      directory_filter: '',
      image_size_options: [
        { text: 'Actual pixels', value: 'actual' },
        { text: '100px', value: 'bound100' },
        { text: '300px', value: 'bound300' },
      ],
      declare: emptyDeclare(),
      declared: {}, // query id -> group label, for this session
      character_class_options: [],
      character_matches: [],
      selected_matches: [],
      book: null,
      items: [],
      total_count: 0,
      image_size: 'bound100',
      per_page: 10,
      page: 1,
      fields: [
        { key: 'query', stickyColumn: true, variant: 'info' },
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
        'match11',
        'match12',
        'match13',
        'match14',
        'match15',
        'match16',
        'match17',
        'match18',
        'match19',
        'match20',
      ],
      existing_matches: [],
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
    current_run() {
      return this.matched_directory
        ? parseMatchDir(this.matched_directory)
        : null
    },
    run_details() {
      return describeRunLong(this.current_run, this.book_title)
    },
    num_pages() {
      return Math.max(1, Math.ceil(this.total_count / this.per_page))
    },
    // Runs as readable labels, grouped by run date (newest first, as the server sorts them),
    // narrowed by the filter box, which matches the label or the raw folder name.
    directory_options() {
      const term = this.directory_filter.trim().toLowerCase()
      const groups = []
      let shown = 0
      for (const d of this.match_directories) {
        const run = parseMatchDir(d.dir)
        const text = run ? describeRunShort(run, this.book_title) : d.dir
        if (
          term &&
          !text.toLowerCase().includes(term) &&
          !d.dir.toLowerCase().includes(term)
        ) {
          continue
        }
        const group_label = run ? run.date : 'Other'
        let group = groups.find((g) => g.label === group_label)
        if (!group) {
          group = { label: group_label, options: [] }
          groups.push(group)
        }
        group.options.push({ value: d.dir, text })
        shown += 1
      }
      const prompt = term
        ? `Select a run (${shown} of ${
            this.match_directories.length
          } match "${this.directory_filter.trim()}")`
        : `Select a run (${this.match_directories.length})`
      return [{ value: null, text: prompt }].concat(groups)
    },
    declare_ready() {
      if (this.declare.matches.length === 0) return false
      return this.declare.new_group
        ? this.declare.label.trim().length > 0
        : !!this.declare.group_id
    },
  },
  methods: {
    char_selected(event) {
      let row_matches = this.selected_matches[event['row_idx']]
      if (row_matches.has(event['id'])) {
        row_matches.delete(event['id'])
      } else {
        row_matches.add(event['id'])
      }
      this.selected_matches.splice(event['row_idx'], 1, row_matches)
      this.save_row_matches(event['row_idx'])
    },
    on_page_change(page) {
      this.page = page
      this.fetch_characters()
    },
    row_candidate_ids(idx) {
      return Object.entries(this.items[idx])
        .filter(([key, value]) => key !== 'query' && !!value)
        .map(([, value]) => value.id)
    },
    // Saved matches are keyed by (book, query) only, not by run, so a query that appears in several
    // runs shares one saved list. Save only the clicked row, and keep matches saved for this query from
    // other runs (any saved id that isn't one of this row's candidates).
    save_row_matches(idx) {
      const query = this.items[idx]['query'].id
      const row_ids = new Set(this.row_candidate_ids(idx))
      const existing = this.existing_matches.find((em) => em['query'] === query)
      const from_other_runs = existing
        ? existing['matches'].filter((id) => !row_ids.has(id))
        : []
      const matches = from_other_runs.concat(
        Array.from(this.selected_matches[idx])
      )
      HTTP.post('/books/' + this.book + `/save_matched_characters/`, {
        matches: [{ query: query, matches: matches }],
      }).then(
        () => {
          if (existing) {
            existing['matches'] = matches
          } else {
            this.existing_matches.push({ query: query, matches: matches })
          }
        },
        (error) => {
          console.log(error)
        }
      )
    },
    copy_dir() {
      navigator.clipboard.writeText(this.matched_directory)
    },
    clear_book() {
      this.book = null
      this.matched_directory = null
      this.matched_character_class = null
      this.match_directories = []
      this.directory_filter = ''
      this.progress_spinner = false
      this.character_class_options = []
      this.total_count = 0
      this.items = []
    },
    update_directories() {
      this.progress_spinner = true
      HTTP.get('/books/' + this.book + '/matched_directories').then(
        (response) => {
          this.match_directories = response.data.match_directories
          this.progress_spinner = false
        },
        (error) => {
          console.log(error)
          this.match_directories = []
          this.progress_spinner = false
        }
      )
    },
    book_selected(event) {
      if (event == null) {
        return
      }
      this.book = event
      this.update_directories()
    },
    directory_selected(event) {
      if (event == null) {
        return
      }
      this.matched_directory = event
      this.matched_character_class = null
      this.items = []
      const directory = this.match_directories.find(
        (d) => d.dir === this.matched_directory
      )
      // the server omits character_classes for a run folder with no letter subfolders,
      // and lists them by folder modification time, so sort them for the dropdown
      const character_classes = (
        (directory && directory.character_classes) ||
        []
      )
        .slice()
        .sort()
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
      const queries = []
      for (const matched_character of matched_characters) {
        const item = {
          query: matched_character['target'],
        }
        queries.push(matched_character['target'].id)
        for (let i = 0; i < matched_character['matches'].length; i++) {
          const match_obj = matched_character['matches'][i]
          if (matched_character['distances']) {
            match_obj['distance'] = matched_character['distances'][i]
          }
          item[`match${i + 1}`] = match_obj
        }
        formatted_items.push(item)
      }
      this.fields = Object.keys(formatted_items[0])
      this.fields[0] = { key: 'query', stickyColumn: true, variant: 'info' }
      this.items = formatted_items
      this.selected_matches = this.items.map(() => new Set())
      this.fetch_existing_matches(queries)
    },
    character_class_selected(event) {
      if (event == null) {
        return
      }
      this.matched_character_class = event
      this.fetch_characters()
    },
    fetch_characters() {
      const offset = (this.page - 1) * this.per_page
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
          if (response.data['matched_characters'].length > 0) {
            this.format_response_for_table(response.data['matched_characters'])
            this.total_count = response.data.total_count
          } else {
            this.items = []
            this.fields = []
            this.selected_matches = []
          }
          this.progress_spinner = false
        },
        (error) => {
          console.log(error)
          this.items = []
          this.fields = []
          this.selected_matches = []
          this.progress_spinner = false
        }
      )
    },
    fetch_existing_matches(queries) {
      return HTTP.post(
        '/books/' + this.book + `/existing_matched_characters/`,
        {
          queries: queries,
        }
      ).then(
        (response) => {
          console.log('existing matched characters: ', response)
          this.existing_matches =
            (response.data && response.data.existing_matches) || []
          this.update_selected_matches()
        },
        (error) => {
          console.log(error)
          this.existing_matches = []
        }
      )
    },
    update_selected_matches() {
      this.items.forEach((item, idx) => {
        let matches = new Set()
        const query = item['query']
        const existing_matches = this.existing_matches.find(
          (em) => em['query'] === query.id
        )
        if (existing_matches !== undefined) {
          for (const [k, v] of Object.entries(item)) {
            if (k === 'query') continue
            const char_id = v.id
            if (existing_matches['matches'].includes(char_id)) {
              matches.add(char_id)
            }
          }
        }
        this.selected_matches.splice(idx, 1, matches)
      })
      console.log('Updated selected matches: ', this.selected_matches)
    },
    open_declare(idx) {
      const item = this.items[idx]
      const query = item['query']
      const ticked = this.selected_matches[idx]
      const matches = Object.entries(item)
        .filter(
          ([key, value]) => key !== 'query' && !!value && ticked.has(value.id)
        )
        .map(([key, value]) => ({
          id: value.id,
          rank: parseInt(key.replace('match', '')),
          distance: value.distance,
          text: `${characterCaption(value)} (rank ${parseInt(
            key.replace('match', '')
          )}, d=${value.distance})`,
          short: characterCaption(value),
        }))
        .sort((a, b) => a.rank - b.rank)
      const query_short = characterCaption(query)
      const run_text = this.current_run
        ? describeRunShort(this.current_run, this.book_title)
        : this.matched_directory
      const today = new Date().toISOString().slice(0, 10)
      this.declare = {
        ...emptyDeclare(),
        show: true,
        query_id: query.id,
        query_text: query_short,
        matches: matches,
        label: `${
          String(query.character_class).split('_')[0]
        } ${query_short} ↔ ${matches.map((m) => m.short).join(', ')}`.slice(
          0,
          200
        ),
        provenance:
          `${today}: declared via Character Matches Review. ` +
          `Run: ${run_text}; letter ${this.matched_character_class}. ` +
          `Query: ${query_short}. ` +
          `Matches: ${matches.map((m) => m.text).join('; ')}. ` +
          `Run folder: ${this.matched_directory}`,
      }
    },
    api_error_text(error) {
      const data = error && error.response && error.response.data
      if (!data) return String(error)
      if (typeof data === 'string') return data
      return Object.entries(data)
        .map(([field, msgs]) => `${field}: ${[].concat(msgs).join(' ')}`)
        .join('; ')
    },
    submit_declare() {
      const characters = [this.declare.query_id].concat(
        this.declare.matches.map((m) => m.id)
      )
      const provenance = this.declare.provenance.trim()
      this.declare.busy = true
      this.declare.error = ''
      let request
      if (this.declare.new_group) {
        const notes = [this.declare.notes.trim(), provenance]
          .filter((s) => s.length > 0)
          .join('\n')
        request = HTTP.post('/character_groupings/', {
          label: this.declare.label.trim(),
          notes: notes,
          characters: characters,
        }).then((response) => response.data)
      } else {
        const id = this.declare.group_id
        request = HTTP.patch(`/character_groupings/${id}/add_characters/`, {
          characters: characters,
        })
          .then(() => HTTP.get(`/character_groupings/${id}/`))
          .then((response) => {
            const notes = (response.data.notes || '').trim()
            return HTTP.patch(`/character_groupings/${id}/`, {
              notes: notes ? `${notes}\n${provenance}` : provenance,
            }).then(() => response.data)
          })
      }
      request.then(
        (group) => {
          this.$set(this.declared, this.declare.query_id, group.label)
          this.$bvToast.toast(
            `Added ${characters.length} glyphs to "${group.label}".`,
            {
              title: 'Match declared',
              variant: 'success',
              to: `/character_groupings/${group.id}`,
              autoHideDelay: 6000,
            }
          )
          this.declare.busy = false
          this.declare.show = false
        },
        (error) => {
          console.log(error)
          this.declare.error = this.api_error_text(error)
          this.declare.busy = false
        }
      )
    },
  },
}
</script>
