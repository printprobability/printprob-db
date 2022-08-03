<template>
  <b-container class="my-2">
    <b-card header="Create a new book">
      <b-form-row>
        <b-col col md="4">
          <b-form-group
            id="vid-group"
            label="VID"
            label-for="vid-input"
            description="Enter the Proquest ID for a known book from EEBO to prepopulate other ID, title, author, publisher, and date fields if already recorded in EEBO."
          >
            <b-form-input
              id="vid-input"
              v-model="vid"
              type="number"
              number
              no-wheel
              debounce="750"
              @input="populate_from_vid($event)"
            />
          </b-form-group>
          <b-form-group
            id="eebo-group"
            label="EEBO id"
            label-for="eebo-input"
            description="Enter an EEBO number to prepopulate other ID, title, author, publisher, and date fields if already recorded in EEBO."
          >
            <b-form-input
              id="eebo-input"
              v-model="eebo"
              type="number"
              number
              no-wheel
              debouce="750"
              @input="populate_from_eebo($event)"
            />
          </b-form-group>
          <b-form-group id="tcp-group" label="tcp" label-for="tcp-input">
            <b-form-input id="tcp-input" v-model="tcp" />
          </b-form-group>
          <b-form-group id="estc-group" label="estc" label-for="estc-input">
            <b-form-input
              id="estc-input"
              v-model="estc"
              debounce="750"
              @input="populate_from_estc($event)"
            />
          </b-form-group>
        </b-col>
        <b-col col md="4">
          <b-form-group id="title-group" label-for="title-input" label="Title">
            <b-form-input
              id="title-input"
              v-model="title"
              required
              :state="title != ''"
            />
          </b-form-group>
          <b-form-group
            id="publisher-group"
            label="Publisher"
            label-for="publisher-input"
            description="Publisher of the book (enter as 'Last name, first name (CERL ID)' using ; to separate multiple names)"
          >
            <b-form-input id="publisher-input" v-model="publisher" />
          </b-form-group>
          <b-form-group
            id="colloquial-printer-group"
            label="Colloquial Printer"
            label-for="colloq-printer-input"
            description="Commonly-held printer identification (enter as 'Last name, first name (CERL ID)' using ; to separate multiple names)"
          >
            <b-form-input id="colloq-printer-input" v-model="colloq_printer" />
          </b-form-group>
          <b-form-group
            id="pp-printer-group"
            label="P&P Printer"
            label-for="pp-printer-input"
            description="The printer as proposed by the P&P team (enter as 'Last name, first name (CERL ID)' using ; to separate multiple names)"
          >
            <b-form-input id="pp-printer-input" v-model="pp_printer" />
          </b-form-group>
          <b-form-group
            id="author-group"
            label-for="author-input"
            label="Author"
          >
            <b-form-input id="author-input" v-model="author" />
          </b-form-group>
          <b-form-group
            id="repository-group"
            label-for="repository-input"
            label="Repository"
          >
            <b-form-input id="repository-input" v-model="repository" />
          </b-form-group>
        </b-col>
        <b-col col md="4">
          <b-form-group id="date-range-group" label="Published between">
            <b-form inline>
              <b-form-input
                class="mx-2"
                id="year-input-early"
                type="date"
                v-model="date_early"
                :state="date_early != ''"
                required
              />and
              <b-form-input
                class="mx-2"
                id="year-input-late"
                type="date"
                v-model="date_late"
                :state="date_late != ''"
                required
              />
            </b-form>
          </b-form-group>
          <b-form-group
            id="pp-notes-group"
            label="Notes"
            label-for="pp-notes-input"
          >
            <b-form-textarea id="pp-notes-input" size="lg" v-model="pp_notes" />
          </b-form-group>
        </b-col>
      </b-form-row>
      <template v-slot:footer>
        <div class="d-flex justify-content-between">
          <b-button variant="warning" @click="cancel">Cancel</b-button>
          <b-button variant="success" @click="submit">Create</b-button>
        </div>
      </template>
    </b-card>
  </b-container>
</template>

<script>
import { HTTP } from '../../main'
import moment from 'moment'
export default {
  name: 'BookCreate',
  data() {
    return {
      eebo: null,
      vid: null,
      tcp: '',
      estc: '',
      title: '',
      publisher: '',
      colloq_printer: '',
      pp_printer: '',
      author: '',
      repository: '',
      date_early: '',
      date_late: '',
      pp_notes: '',
    }
  },
  methods: {
    cancel() {
      this.$router.push({ name: 'BookListView' })
    },
    date_to_number(d) {
      return Number(moment(new Date(d)).format('YYYY'))
    },
    populate(
      retrieved_book,
      update_vid = true,
      update_eebo = true,
      update_estc = true
    ) {
      this.$bvToast.toast(`Data retrieved`, {
        title: retrieved_book.pq_title,
        autoHideDelay: 5000,
        appendToast: true,
        variant: 'success',
      })
      if (update_vid) {
        this.vid = retrieved_book.vid
      }
      if (update_eebo) {
        this.eebo = retrieved_book.eebo
      }
      if (update_estc) {
        this.estc = retrieved_book.estc
      }
      this.tcp = retrieved_book.tcp
      this.title = retrieved_book.pq_title
      this.publisher = !!retrieved_book.pq_publisher
        ? retrieved_book.pq_publisher
        : retrieved_book.pp_publisher
      this.author = !!retrieved_book.pq_author
        ? retrieved_book.pq_author
        : retrieved_book.pp_author
      this.repository = retrieved_book.repository
      this.colloq_printer = retrieved_book.colloq_printer
      this.date_early = `${retrieved_book.pq_year_early}-01-01`
      this.date_late = `${retrieved_book.pq_year_late}-12-31`
    },
    populate_from_vid(vid) {
      if (!!vid) {
        HTTP.get('/books/', { params: { vid: vid } }).then(
          (response) => {
            if (response.data.count >= 1) {
              const retrieved_book = response.data.results[0]
              this.populate(retrieved_book, { skip_vid: true })
            } else {
              this.$bvToast.toast(`Failed`, {
                title: `No book with VID ${vid}`,
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'warning',
              })
            }
          },
          (error) => {
            this.$bvToast.toast(error, {
              title: 'Error',
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger',
            })
          }
        )
      }
    },
    populate_from_eebo(eebo) {
      if (!!eebo) {
        HTTP.get('/books/', { params: { eebo: eebo } }).then(
          (response) => {
            if (response.data.count >= 1) {
              const retrieved_book = response.data.results[0]
              this.populate(retrieved_book, { skip_eebo: true })
            } else {
              this.$bvToast.toast(`Failed`, {
                title: `No book with EEBO ${eebo}`,
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'warning',
              })
            }
          },
          (error) => {
            this.$bvToast.toast(error, {
              title: 'Error',
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger',
            })
          }
        )
      }
    },
    populate_from_estc(estc) {
      if (!!estc) {
        HTTP.get('/books/', { params: { estc: estc } }).then(
          (response) => {
            if (response.data.count >= 1) {
              const retrieved_book = response.data.results[0]
              this.populate(retrieved_book, { skip_estc: true })
            } else {
              this.$bvToast.toast(`Failed`, {
                title: `No book with ESTC ${estc}`,
                autoHideDelay: 5000,
                appendToast: true,
                variant: 'warning',
              })
            }
          },
          (error) => {
            this.$bvToast.toast(error, {
              title: 'Error',
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger',
            })
          }
        )
      }
    },
    submit() {
      const payload = {
        eebo: this.eebo,
        vid: this.vid,
        tcp: this.tcp,
        estc: this.estc,
        pq_title: this.title,
        pp_publisher: this.publisher,
        colloq_printer: this.colloq_printer,
        pp_printer: this.pp_printer,
        pp_author: this.author,
        repository: this.repository,
        pq_year_early: this.date_to_number(this.date_early),
        pq_year_late: this.date_to_number(this.date_late),
        date_early: this.date_early,
        date_late: this.date_late,
        pp_notes: this.pp_notes,
      }
      HTTP.post('/books/', payload).then(
        (response) => {
          this.$bvToast.toast(`Book created`, {
            title: response.data.pq_title,
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'success',
          })
          this.$router.push({
            name: 'BookDetailView',
            params: { id: response.data.id },
          })
        },
        (error) => {
          for (let [k, v] of Object.entries(error.response.data)) {
            this.$bvToast.toast(v, {
              title: error.response.status + ': ' + k,
              autoHideDelay: 5000,
              appendToast: true,
              variant: 'danger',
            })
          }
        }
      )
    },
  },
}
</script>
