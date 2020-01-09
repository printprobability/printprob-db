<template>
  <div>
    <b-pagination
      v-model="spread"
      :total-rows="n_spreads"
      :per-page="1"
      aria-controls="spread-results"
    />
    <h4>Spread {{ spread }}</h4>
    <div class="row">
      <div v-if="lines" class="col-6">
        <h5>Left page</h5>
        <ol v-if="!!lines.l">
          <li v-for="line in lines.l" :key="line.id">
            <LineImage :line="line"></LineImage>
          </li>
        </ol>
        <p v-else>No lines extracted for this page</p>
      </div>
      <div class="col-6">
        <h5>Right page</h5>
        <ol v-if="!!lines.r">
          <li v-for="line in lines.r" :key="line.id">
            <LineImage :line="line"></LineImage>
          </li>
        </ol>
        <p v-else>No lines extracted for this page</p>
      </div>
    </div>
  </div>
</template>

<script>
import LineImage from "../Lines/LineImage";
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "LineList",
  components: {
    LineImage
  },
  props: {
    n_spreads: Number,
    line_run_id: String
  },
  data() {
    return {
      lines: {},
      spread: 1
    };
  },
  methods: {
    get_line_run: function(id, spread) {
      return HTTP.get("/lines/", {
        params: { created_by_run: id, spread_sequence: spread }
      }).then(
        response => {
          this.lines = _.groupBy(response.data.results, "page_side");
        },
        error => {
          console.log(error);
        }
      );
    }
  },
  watch: {
    spread: function() {
      this.get_line_run(this.line_run_id, this.spread);
    }
  },
  created() {
    this.get_line_run(this.line_run_id, this.spread);
  }
};
</script>
