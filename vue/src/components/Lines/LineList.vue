<template>
  <div>
    <b-pagination
      v-model="sequence"
      :total-rows="n_pages - 1"
      :per-page="1"
      aria-controls="page-results"
    />
    <h4>Page {{ sequence }}</h4>
    <div class="row">
      <div v-if="lines" class="col-6">
        <ol>
          <li v-for="line in lines" :key="line.id">
            <LineImage :line="line"></LineImage>
          </li>
        </ol>
      </div>
      <p v-else>No lines extracted for this page</p>
    </div>
  </div>
</template>

<script>
import LineImage from '../Lines/LineImage'
import { HTTP } from '../../main'

export default {
  name: 'LineList',
  components: {
    LineImage,
  },
  props: {
    n_pages: Number,
    line_run_id: String,
  },
  data() {
    return {
      lines: [],
      sequence: 0,
    }
  },
  methods: {
    get_line_run: function (id, sequence) {
      return HTTP.get('/lines/', {
        params: { created_by_run: id, page_sequence: sequence },
      }).then(
        (response) => {
          this.lines = response.data.results
        },
        (error) => {
          console.log(error)
        }
      )
    },
  },
  watch: {
    sequence: function () {
      this.get_line_run(this.line_run_id, this.sequence)
    },
  },
  created() {
    this.get_line_run(this.line_run_id, this.sequence)
  },
}
</script>
