<template>
  <b-form-group :label="label" :description="description" label-size="sm">
    <VueBootstrapTypeahead
      size="sm"
      :data="results"
      :value="value"
      :serializer="serializer"
      :placeholder="placeholder"
      @hit="selected=$event"
      @input="search_text=$event"
      :maxMatches="Number(n_choices)"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from "../../main";
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";
import _ from "lodash";

const AUTOCOMPLETE_DEBOUNCE_TIME = 500

export default {
  name: "Autocomplete",
  components: {
    VueBootstrapTypeahead
  },
  props: {
    value: {
      type: String,
      default: ""
    },
    endpoint: String,
    query_field: String,
    label: String,
    description: {
      type: String,
      default: null
    },
    placeholder: {
      type: String,
      default: null
    },
    display_field: {
      type: String,
      default: "label"
    },
    n_choices: {
      type: String,
      default: "10"
    },
    prefix_field: {
      type: String,
      default: null
    },
    return_field: String,
    additional_params: Object
  },
  data() {
    return {
      results: [],
      search_text: "",
      selected: null
    };
  },
  methods: {
    get_results: _.debounce(function(query) {
      var payload = { params: { limit: this.n_choices } };
      payload.params[this.query_field] = query;
      for (var attrname in this.additional_params) {
        payload.params[attrname] = this.additional_params[attrname];
      }
      HTTP.get(this.endpoint, payload).then(
        results => {
          if (results.data.count > 0) {
            this.results = results.data.results;
          } else {
            var empty_result = {};
            empty_result[this.display_field] = "No results";
            this.results.push();
          }
        },
        error => {
          console.log(error);
        }
      );
    }, AUTOCOMPLETE_DEBOUNCE_TIME),
    serializer: function(x) {
      if (!!this.prefix_field) {
        return (
          this.prefix_field +
          " " +
          x[this.prefix_field] +
          ": " +
          x[this.display_field]
        );
      } else {
        return x[this.display_field];
      }
    },
    clear() {
      this.results = [];
      this.search_text = "";
      this.selected = null;
    }
  },
  watch: {
    search_text: function(txt) {
      this.get_results(txt);
    },
    selected() {
      if (!!this.selected) {
        this.$emit("input", this.selected[this.return_field]);
      }
    }
  }
};
</script>
