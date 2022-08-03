<template>
  <div>
    <b-row>
      <b-col cols="12">
        <b-card header="Title">
          <b-form-textarea
            required
            v-model="book.pq_title"
            :plaintext="readonly"
            @blur="conditional_edit_group('pq_title', book.pq_title)"
          />
        </b-card>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-card header="Identifiers">
          <b-row align-h="between" class="px-3">
            <dl>
              <dt>P&P id</dt>
              <dd>{{ book.id }}</dd>
            </dl>
            <b-form-group
              id="eebo-group"
              label="EEBO id"
              label-for="eebo-input"
            >
              <b-form-input
                :plaintext="readonly"
                id="eebo-input"
                type="number"
                v-model="book.eebo"
                @blur="conditional_edit_group('eebo', book.eebo)"
              />
            </b-form-group>
            <b-form-group id="vid-group" label="VID" label-for="vid-input">
              <b-form-input
                :plaintext="readonly"
                id="vid-input"
                type="number"
                v-model="book.vid"
                @blur="conditional_edit_group('vid', book.vid)"
              />
            </b-form-group>
            <b-form-group id="tcp-group" label="TCP id" label-for="tcp-input">
              <b-form-input
                :plaintext="readonly"
                id="tcp-input"
                v-model="book.tcp"
                @blur="conditional_edit_group('tcp', book.tcp)"
              />
            </b-form-group>
            <b-form-group
              id="estc-group"
              label="ESTC id"
              label-for="estc-input"
            >
              <b-form-input
                :plaintext="readonly"
                id="estc-input"
                v-model="book.estc"
                @blur="conditional_edit_group('estc', book.estc)"
              />
            </b-form-group>
          </b-row>
        </b-card>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="6">
        <b-card header="EEBO Metadata">
          <dl>
            <dt>Publisher</dt>
            <dd>{{ book.pq_publisher }}</dd>
            <dt>Author:</dt>
            <dd>{{ book.pq_author }}</dd>
            <div>
              <dt v-if="book.pq_url">Proquest link</dt>
              <dd>
                <a :href="book.pq_url">{{ book.pq_url }}</a>
              </dd>
            </div>
          </dl>
        </b-card>
      </b-col>
      <b-col cols="6">
        <b-card header="P&P Metadata">
          <b-form-group
            id="repository-group"
            label="Repository"
            label-for="repository-input"
          >
            <b-form-input
              id="repository-input"
              v-model="book.repository"
              @blur="edit_group('repository', book.repository)"
            />
          </b-form-group>
          <b-form-group
            id="publisher-group"
            label="Publisher"
            label-for="publisher-input"
          >
            <b-form-input
              id="publisher-input"
              v-model="book.pp_publisher"
              @blur="edit_group('pp_publisher', book.pp_publisher)"
            />
          </b-form-group>
          <b-form-group
            id="colloq-printer-group"
            label="Commonly-known printer"
            label-for="colloq-printer-input"
          >
            <b-form-input
              id="colloq-printer-input"
              v-model="book.colloq_printer"
              @blur="edit_group('colloq_printer', book.colloq_printer)"
            />
          </b-form-group>
          <b-form-group
            id="pp-printer-group"
            label="P&P Printer"
            label-for="pp-printer-input"
          >
            <b-form-input
              id="pp-printer-input"
              v-model="book.pp_printer"
              @blur="edit_group('pp_printer', book.pp_printer)"
            />
          </b-form-group>
          <b-form-group
            id="author-group"
            label="Author"
            label-for="author-input"
          >
            <b-form-input
              id="author-input"
              v-model="book.pp_author"
              @blur="edit_group('pp_author', book.pp_author)"
            />
          </b-form-group>
          <b-form-group
            id="created-early-group"
            label="Created no earlier than"
            label-for="created-early-input"
          >
            <b-form-input
              type="date"
              id="created-early-input"
              v-model="book.date_early"
              @blur="edit_group('date_early', book.date_early)"
            />
          </b-form-group>
          <b-form-group
            id="created-late-group"
            label="Created no later than"
            label-for="created-late-input"
          >
            <b-form-input
              type="date"
              id="created-late-input"
              v-model="book.date_late"
              @blur="edit_group('date_late', book.date_late)"
            />
          </b-form-group>
          <b-form-group
            id="pp-notes-group"
            label="Notes"
            label-for="pp-notes-input"
          >
            <b-form-textarea
              id="pp-notes-input"
              size="lg"
              v-model="book.pp_notes"
              @blur="edit_group('pp_notes', book.pp_notes)"
            />
          </b-form-group>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { HTTP } from '../../main'

export default {
  name: 'BookDetailEdit',
  props: {
    book: null,
  },
  computed: {
    readonly() {
      return this.book.is_eebo_book
    },
  },
  methods: {
    conditional_edit_group(fieldname, content) {
      if (!this.readonly) {
        this.edit_group(fieldname, content)
      }
    },
    edit_group: function (fieldname, content) {
      var payload = {}
      payload[fieldname] = content
      return HTTP.patch('/books/' + this.book.id + '/', payload).then(
        (response) => {
          this.$bvToast.toast(`${fieldname} updated`, {
            title: response.data.id,
            autoHideDelay: 5000,
            appendToast: true,
            variant: 'success',
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
