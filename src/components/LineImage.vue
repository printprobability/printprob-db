<template>
  <p>
    <img
      :src="line.pref_image.web_url"
      class="line-image my-3 mx-auto"
      :class="{'selected-line-image': line.pref_image.bad_capture}"
      @click="toggleClassification(line)"
    >
    <span>{{ line.pref_image.pk }}</span>
  </p>
</template>

<script>
export default {
  name: "LineImage",
  props: {
    line: Object
  },
  methods: {
    addClassification: function(pk) {
      var payload = {
        image: pk
      };
      return axios.post("http://localhost:4000/captures/", payload).then(
        response => {
          console.log(response);
        },
        errors => {
          console.log(errors);
        }
      );
    },
    removeClassification: function(pk) {
      return axios.delete("http://localhost:4000/captures/" + pk).then(
        response => {
          console.log(response);
        },
        errors => {
          console.log(errors);
        }
      );
    },
    toggleClassification: function(line) {
      var img = line.pref_image;
      console.log(img.bad_capture);
      if (img.bad_capture) {
        var reqres = this.removeClassification(img.pk);
      } else {
        var reqres = this.addClassification(img.pk);
      }
      img.bad_capture = !img.bad_capture;
      return reqres;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img.line-image {
  max-width: 800px;
  border: 2px solid black;
}
img.selected-line-image {
  border: 3px solid red;
  filter: blur(5px);
}
</style>
