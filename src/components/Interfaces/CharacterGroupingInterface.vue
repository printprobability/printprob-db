<template>
  <div class="container-fluid">
    <h1 class="my-2">Compose Character Groups</h1>
    <p
      class="my-2"
    >Add and edit custom character groups here. Browse all characters on the left. On the right, select an existing character grouping or make a new one, and then click on characters to add them.</p>
    <div class="row">
      <div class="col-7">
        <CharacterList
          :highlighted_characters="intersecting_images"
          :page="page"
          @page_input="page=$event"
          :character_class="character_class"
          @character_class_input="character_class=$event"
          :book="book"
          @book_input="book=$event"
          :char_agreement="char_agreement"
          @char_agreement_input="char_agreement=$event"
          :order="order"
          @order_input="order=$event"
          :character_run="character_run"
          @character_run_input="character_run=$event"
          v-model="displayed_images"
          @char_clicked="register_character"
        />
      </div>
      <div class="col-5">
        <div class="card sticky-top">
          <div class="card-header">
            <div class="d-inline-flex align-items-center">
              <b-button
                @click="toggle_create"
                size="sm"
                class="mr-2"
                :variant="new_cg_card.button_variant[new_cg_card.show]"
              >{{ new_cg_card.button_text[new_cg_card.show] }}</b-button>
              <CharacterGroupingSelect v-model="cg_id" :key="cg_menu_key" />
            </div>
            <NewCharacterGrouping v-show="new_cg_card.show" @new_group="create_group" />
          </div>
          <div class="card-body" v-if="selected_cg">
            <dl class="row">
              <dt class="col-sm-3">Label</dt>
              <dd
                class="col-sm-9"
                contenteditable="contenteditable"
                @blur="edit_group(selected_cg.id, 'label', $event.target.innerText)"
              >{{ selected_cg.label }}</dd>

              <dt class="col-sm-3">Notes</dt>
              <dd
                class="col-sm-9"
                contenteditable="contenteditable"
                @blur="edit_group(selected_cg.id, 'notes', $event.target.innerText)"
              >{{ selected_cg.notes }}</dd>
            </dl>
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
            <b-alert v-else show variant="info">This group has no characters yet.</b-alert>
          </div>
          <div class="card-footer d-flex justify-content-between" v-if="selected_cg">
            <small>Created by {{ selected_cg.created_by }} on {{ display_date(selected_cg.date_created) }}</small>
            <b-button
              variant="info"
              size="sm"
              :href="$APIConstants.PP_ENDPOINT + '/character_groupings/' + cg_id + '/download/'"
            >Download ZIP</b-button>
            <b-button v-b-modal.delete-modal variant="danger" size="sm">Delete</b-button>
            <b-modal
              id="delete-modal"
              title="Delete group?"
              ok-variant="danger"
              ok-title="Delete"
              @ok="delete_group"
            >
              <p>Are you sure? This can't be undone.</p>
            </b-modal>
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
      cg_id: null,
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
      cg_menu_key: 0,
      page: 1,
      book: null,
      character_class: null,
      order: "-class_probability",
      character_run: null,
      char_agreement: "all"
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
    register_character: function(char_id) {
      if (!!this.cg_id) {
        // Send the add request to the endpoint
        return HTTP.patch(
          "/character_groupings/" + this.cg_id + "/add_characters/",
          { characters: [char_id] }
        ).then(
          response => {
            response;
            // If it worked, update the character grouping view
            this.get_cg(this.cg_id);
          },
          error => {
            console.log(error);
          }
        );
      }
    },
    deregister_character: function(char_id) {
      if (!!this.cg_id) {
        // Send the add request to the endpoint
        return HTTP.patch(
          "/character_groupings/" + this.cg_id + "/delete_characters/",
          { characters: [char_id] }
        ).then(
          response => {
            response;
            // If it worked, update the character grouping view
            this.get_cg(this.cg_id);
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
      this.new_cg_card.show = false;
      const payload = {
        label: obj.label,
        notes: obj.notes,
        characters: []
      };
      return HTTP.post("/character_groupings/", payload).then(
        response => {
          this.refresh_cg_menu();
          this.cg_id = response.data.id;
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
          this.cg_id = null;
          this.selected_cg = null;
        },
        error => {
          console.log(error);
        }
      );
    },
    edit_group: function(id, field, content) {
      var payload = {};
      payload[field] = content;
      return HTTP.patch("/character_groupings/" + id + "/", payload).then(
        response => {
          this.refresh_cg_menu();
          this.cg_id = response.data.id;
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
    cg_id: function(id) {
      this.get_cg(id);
    }
  }
};
</script>