<template>
  <div>
    <b-row>
      <b-col cols="12">
        <b-card header="Title">{{ book.pq_title }}</b-card>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-card header="Identifiers">
          <b-row align-h="between" class="px-3">
            <dl>
              <dt>P&P id</dt>
              <dd>{{ book.id }}</dd>
              <dt>EEBO</dt>
              <dd>{{ book.eebo }}</dd>
              <dt>VID</dt>
              <dd>{{ book.vid }}</dd>
              <dt>TCP</dt>
              <dd>{{ book.tcp }}</dd>
              <dt>ESTC</dt>
              <dd>{{ book.estc }}</dd>
            </dl>
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

            <dt>Bridges images</dt>
            <dd>
              <code>/pylon5/hm560ip/djevans/eebo_unzipped/{{ book.zipfile }}/{{ book.vid }}/</code>
            </dd>
            <dt>Proquest link</dt>
            <dd>
              <a :href="book.pq_url">{{ book.pq_url }}</a>
            </dd>
          </dl>
        </b-card>
      </b-col>
      <b-col cols="6">
        <b-card header="P&P Metadata">
          <dl>
            <dt>Publisher</dt>
            <dd>{{ book.pp_publisher }}</dd>
            <dt>Created no earlier than</dt>
            <dd>{{ book.date_early }}</dd>
            <dt>Created no later than</dt>
            <dd>{{ book.date_late}}</dd>
          </dl>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: "BookDetailDisplay",
  props: {
    book: null
  }
};
</script>