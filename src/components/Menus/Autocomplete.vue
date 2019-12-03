<template>
  <b-form-group :label="label" :description="description">
    <VueBootstrapTypeahead
      :data="results"
      :value="value"
      :serializer="serializer"
      :placeholder="placeholder"
      @hit="selected = $event"
      @input="search_text=$event"
    />
  </b-form-group>
</template>

<script>
import { HTTP } from "../../main";
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";
import _ from "lodash";

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
      HTTP.get(this.endpoint, payload).then(
        results => {
          this.results = results.data.results;
        },
        error => {
          console.log(error);
        }
      );
    }, 500),
    serializer: function(x) {
      return x[this.display_field];
    }
  },
  watch: {
    search_text: function(txt) {
      this.get_results(txt);
    },
    selected() {
      this.$emit("input", this.selected[this.return_field]);
    }
  }
};
</script>
