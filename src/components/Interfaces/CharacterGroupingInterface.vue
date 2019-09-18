<template>
  <div class="container">
    <h1>Compose Character Groups</h1>
    <div class="card">
      <p>Add and edit custom character groups here. Browse all characters on the left. On the right, select an existing character grouping or make a new one, and then click on characters to add them.</p>
    </div>
    <div class="row">
      <div class="col-8">
        <CharacterList @update="update_displayed_images" />
      </div>
      <div class="col-4">
        <div class="card">
          <div class="card-body">
            <CharacterGroupingSelect @selected="set_cg" />
            <CharacterGrouping :cg="selected_cg" />
            <b-list-group v-if="selected_cg">
              <template v-for="character in selected_cg.characters">
                <b-list-item :key="character.id">
                  <CharacterImage
                    :character="character"
                    :highlight="intersecting_images.includes(character.id)"
                  />
                </b-list-item>
              </template>
            </b-list-group>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CharacterGroupingSelect from "../Menus/CharacterGroupingSelect";
import CharacterGrouping from "../CharacterGroups/CharacterGrouping";
import CharacterImage from "../Characters/CharacterImage";
import CharacterList from "../Characters/CharacterList";
import { HTTP } from "../../main";
import _ from "lodash";

export default {
  name: "CharacterGroupingInterface",
  components: {
    CharacterGroupingSelect,
    CharacterGrouping,
    CharacterImage,
    CharacterList
  },
  data() {
    return {
      cg_id: null,
      selected_cg: null,
      displayed_images: []
    };
  },
  computed: {
    intersecting_images: function() {
      var cg_ids = this.selected_cg.characters.map(c => c.id);
      var ls_ids = this.displayed_images.map(c => c.id);
      if ((cg_ids.length > 0) & (ls_ids.length > 0)) {
        return _.intersection(cg_ids, ls_ids);
      } else {
        return [];
      }
    }
  },
  methods: {
    get_cg: function(pk) {
      return HTTP.get("/character_groupings/" + pk + "/").then(
        response => {
          this.selected_cg = response.data;
        },
        error => {
          console.log(error);
        }
      );
    },
    set_cg: function(cg_id) {
      this.cg_id = cg_id;
    },
    update_displayed_images: function(imgs) {
      this.displayed_images = imgs;
    }
  },
  watch: {
    cg_id: function(id) {
      this.get_cg(id);
    }
  }
};
</script>