<template>
  <p>
    <img
      :src="line.image.web_url"
      class="line-image my-3 mx-auto"
      @click="toggleClassification(line)"
    />
  </p>
</template>

<script>
export default {
  name: "LineImage",
  props: {
    line: Object
  },
  methods: {
    addClassification: function(id) {
      var payload = {
        image: id
      };
      return this.$http.post("http://localhost/captures/", payload).then(
        response => {
          console.log(response);
        },
        errors => {
          console.log(errors);
        }
      );
    },
    removeClassification: function(id) {
      return this.$http.delete("http://localhost/captures/" + id).then(
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
        var reqres = this.removeClassification(img.id);
      } else {
        var reqres = this.addClassification(img.id);
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
