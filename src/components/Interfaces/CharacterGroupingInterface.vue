<template>
  <div class="container">
    <h1 class="my-2">Compose Character Groups</h1>
    <p
      class="my-2"
    >Add and edit custom character groups here. Browse all characters on the left. On the right, select an existing character grouping or make a new one, and then click on characters to add them.</p>
    <div class="row">
      <div class="col-7">
        <CharacterList
          :highlighted_characters="intersecting_images"
          @update="update_displayed_images"
          @char_clicked="register_character"
        />
      </div>
      <div class="col-5">
        <div class="card">
          <div class="card-header">
            <div class="d-inline-flex align-items-center">
              <b-button
                @click="toggle_create"
                size="sm"
                class="mr-2"
                :variant="new_cg_card.button_variant[new_cg_card.show]"
              >{{ new_cg_card.button_text[new_cg_card.show] }}</b-button>
              <CharacterGroupingSelect v-model="selected_cg_id" :key="cg_menu_key" />
            </div>
            <NewCharacterGrouping v-if="new_cg_card.show" @new_group="create_group" />
          </div>
          <div class="card-body">
            <div class="card" v-if="selected_cg">
              <div class="card-body">
                <p>
                  <strong v-if="selected_cg.notes">Notes:</strong>
                  {{ selected_cg.notes }}
                </p>
                <div
                  class="d-flex flex-wrap justify-content-around"
                  v-if="selected_cg.characters.length>0"
                >
                  <CharacterImage
                    v-for="character in selected_cg.characters"
                    :key="character.id"
                    :character="character"
                    :highlight="intersecting_images.includes(character.id)"
                    @char_clicked="deregister_character"
                  />
                </div>
                <div v-else class="card my-2">This group has no characters yet.</div>
              </div>
              <div class="card-footer d-flex justify-content-between">
                <small>Created by {{ selected_cg.created_by }} on {{ display_date(selected_cg.date_created) }}</small>
                <b-button @click="delete_group" variant="danger" size="sm">Delete</b-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CharacterGroupingSelect from "../Menus/CharacterGroupingSelect";
import NewCharacterGrouping from "../CharacterGroups/NewCharacterGrouping";
import CharacterImage from "../Characters/CharacterImage";
import CharacterList from "../Characters/CharacterList";
import { HTTP } from "../../main";
import moment from "moment";
import _ from "lodash";

export default {
  name: "CharacterGroupingInterface",
  components: {
    CharacterGroupingSelect,
    NewCharacterGrouping,
    CharacterImage,
    CharacterList
  },
  data() {
    return {
      selected_cg_id: null,
      selected_cg: null,
      displayed_images: [],
      new_cg_card: {
        show: false,
        button_variant: {
          false: "primary",
          true: "warning"
        },
        button_text: {
          false: "New",
          true: "Cancel"
        }
      },
      cg_menu_key: 0
    };
  },
  computed: {
    intersecting_images: function() {
      if (!!this.selected_cg & !!this.displayed_images) {
        var cg_ids = this.selected_cg.characters.map(c => c.id);
        var ls_ids = this.displayed_images.map(c => c.id);
        return _.intersection(cg_ids, ls_ids);
      } else {
        return [];
      }
    }
  },
  methods: {
    display_date: function(date) {
      return moment(new Date(date)).format("MM-DD-YY, h:mm a");
    },
    get_cg: function(pk) {
      if (!!pk) {
        return HTTP.get("/character_groupings/" + pk + "/").then(
          response => {
            this.selected_cg = response.data;
          },
          error => {
            console.log(error);
          }
        );
      }
    },
    update_displayed_images: function(imgs) {
      this.displayed_images = imgs;
    },
    register_character: function(char_id) {
      if (!!this.selected_cg_id) {
        // Send the add request to the endpoint
        return HTTP.patch(
          "/character_groupings/" + this.selected_cg_id + "/add_characters/",
          { characters: [char_id] }
        ).then(
          response => {
            response;
            // If it worked, update the character grouping view
            this.get_cg(this.selected_cg_id);
          },
          error => {
            console.log(error);
          }
        );
      }
    },
    deregister_character: function(char_id) {
      if (!!this.selected_cg_id) {
        // Send the add request to the endpoint
        return HTTP.patch(
          "/character_groupings/" + this.selected_cg_id + "/delete_characters/",
          { characters: [char_id] }
        ).then(
          response => {
            response;
            // If it worked, update the character grouping view
            this.get_cg(this.selected_cg_id);
          },
          error => {
            console.log(error);
          }
        );
      }
    },
    toggle_create: function() {
      this.new_cg_card.show = !this.new_cg_card.show;
    },
    create_group: function(obj) {
      var payload = {
        label: obj.label,
        notes: obj.notes,
        characters: []
      };
      return HTTP.post("/character_groupings/", payload).then(
        response => {
          this.refresh_cg_menu();
          this.selected_cg_id = response.data.id;
          this.show_new_cg_card = false;
        },
        error => {
          console.log(error);
        }
      );
    },
    delete_group: function() {
      return HTTP.delete(
        "/character_groupings/" + this.selected_cg.id + "/"
      ).then(
        response => {
          console.log(response);
          this.refresh_cg_menu();
          this.selected_cg_id = null;
          this.selected_cg = null;
        },
        error => {
          console.log(error);
        }
      );
    },
    refresh_cg_menu: function() {
      this.cg_menu_key += 1;
    }
  },
  watch: {
    selected_cg_id: function(id) {
      this.get_cg(id);
    }
  }
};
</script>