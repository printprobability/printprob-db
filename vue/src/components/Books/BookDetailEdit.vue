<template>
  <div>
    <b-row>
      <b-col cols="12">
        <b-card header="Identifiers">
          <b-row align-h="between" class="px-3">
            <dl>
              <dt>P&P id</dt>
              <dd>{{ book.id }}</dd>
            </dl>
            <b-form-group id="eebo-group" label="EEBO id" label-for="eebo-input">
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
            <b-form-group id="estc-group" label="ESTC id" label-for="estc-input">
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
      <b-col cols="12">
        <b-card header="Title">
          <b-form-textarea
            required
            v-model="book.pq_title"
            :plaintext="readonly"
            @blur="edit_group('pq_title', book.pq_title)"
          />
        </b-card>
      </b-col>
    </b-row>
    <b-row>
      <b-card header="EEBO Metadata">
        <dl>
          <dt>Publisher</dt>
          <dd>{{ book.pq_publisher }}</dd>
          <dt>Author:</dt>
          <dd>{{ book.pq_author }}</dd>

          <dt>Bridges zipfiles</dt>
          <dd>
            <code>unzip -d . {{ book.zipfile }}.zip {{ book.zipfile }}/{{ book.vid }}/*</code>
          </dd>
          <dt>Proquest link</dt>
          <dd>
            <a :href="book.pq_url">{{ book.pq_url }}</a>
          </dd>
        </dl>
      </b-card>
      <b-card header="P&P Metadata">
        <b-form-group id="publisher-group" label="Publisher" label-for="publisher-input">
          <b-form-input
            id="publisher-input"
            v-model="book.pp_publisher"
            @blur="edit_group('pp_publisher', book.pp_publisher)"
          />
        </b-form-group>
        <b-form-group
          id="created-early-group"
          label="Created no earlier"
          label-for="created-early-input"
        >
          <b-form-input
            type="date"
            id="created-early-input"
            v-model="book.date_early"
            @blur="edit_group('date_early', book.date_early)"
          />
        </b-form-group>
        <b-form-group id="created-late-group" label="publisher" label-for="created-late-input">
          <b-form-input
            type="date"
            id="created-late-input"
            v-model="book.date_late"
            @blur="edit_group('date_late', book.date_late)"
          />
        </b-form-group>
      </b-card>
    </b-row>
  </div>
</template>

<script>
import { HTTP } from "../../main";

export default {
  name: "BookDetailEdit",
  props: {
    book: null
  },
  computed: {
    readonly() {
      return this.book.is_eebo_book;
    }
  },
  methods: {
    conditional_edit_group(fieldname, content) {
      if (!this.readonly) {
        this.edit_group(fieldname, content);
      }
    },
    edit_group: function(fieldname, content) {
      console.log(content);
      var payload = {};
      payload[fieldname] = content;
      return HTTP.patch("/books/" + this.book.id + "/", payload).then(
        response => {
          this.$bvToast.toast(`${fieldname} updated`, {
            title: response.data.id,
            autoHideDelay: 5000,
            appendToast: true,
            variant: "success"
          });
        },
        error => {
          for (let [k, v] of Object.entries(error.response.data)) {
            this.$bvToast.toast(v, {
              title: error.response.status + ": " + k,
              autoHideDelay: 5000,
              appendToast: true,
              variant: "danger"
            });
          }
        }
      );
    }
  }
};
</script>