<template>
  <div class="container-fluid">
    <h1 class="my-2">Compose Character Groups</h1>
    <p class="my-2">
      Add and edit custom character groups here. Browse all characters on the
      left. On the right, select an existing character grouping or make a new
      one, and then click on characters to add them.
    </p>
    <div class="row">
      <div class="col-7">
        <CharacterList
          :highlighted_characters="intersecting_images"
          :character_class="character_class"
          @character_class_input="character_class = $event"
          :book="book"
          @book_input="book = $event"
          :order="order"
          @order_input="order = $event"
          :char_agreement="char_agreement"
          @char_agreement_input="char_agreement = $event"
          :character_run="character_run"
          @character_run_input="character_run = $event"
          :show_damaged_characters="show_damaged_characters"
          @damaged_characters_input="show_damaged_characters = $event"
          v-model="displayed_images"
          @char_clicked="register_character"
          :input_page_start="page_start"
          :input_page_end="page_end"
          @page_range_input="update_page_range"
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
                >{{ new_cg_card.button_text[new_cg_card.show] }}
              </b-button>
              <CharacterGroupingSelect v-model="cg_id" :key="cg_menu_key" />
            </div>
            <NewCharacterGrouping
              v-show="new_cg_card.show"
              @new_group="create_group"
            />
          </div>
          <div class="card-body" v-if="selected_cg">
            <dl class="row">
              <dt class="col-sm-3">
                <router-link
                  :to="{
                    name: 'CharacterGroupingDetail',
                    params: { id: selected_cg.id },
                  }"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Open in separate page
                </router-link>
              </dt>
              <dt class="col-sm-3">
                <router-link
                  :to="{
                    name: 'CharacterGroupingDetail',
                    params: { id: selected_cg.id },
                    query: { edit: true },
                  }"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Edit in separate page
                </router-link>
              </dt>
            </dl>
            <dl class="row">
              <dt class="col-sm-3">Label</dt>
              <dd
                class="col-sm-9"
                contenteditable="contenteditable"
                @blur="
                  edit_group(selected_cg.id, 'label', $event.target.innerText)
                "
              ></dd>

              <dt class="col-sm-3">Notes</dt>
              <dd
                class="col-sm-9"
                contenteditable="contenteditable"
                @blur="
                  edit_group(selected_cg.id, 'notes', $event.target.innerText)
                "
              >
                {{ selected_cg.notes }}
              </dd>
            </dl>

            <div
              class="d-flex flex-wrap justify-content-around"
              v-if="selected_cg.characters.length > 0"
            >
              <CharacterImage
                v-for="character in selected_cg_ordered_chars"
                :key="character.id"
                :character="character"
                :highlight="intersecting_images.includes(character.id)"
                @char_double_clicked="deregister_character"
              />
            </div>
            <b-alert v-else show variant="info"
              >This group has no characters yet.
            </b-alert>
          </div>
          <div
            class="card-footer d-flex justify-content-between"
            v-if="selected_cg"
          >
            <small
              >Created by {{ selected_cg.created_by }} on
              {{ display_date(selected_cg.date_created) }}</small
            >
            <b-button
              variant="info"
              size="sm"
              :href="
                $APIConstants.PP_ENDPOINT +
                '/character_groupings/' +
                cg_id +
                '/download/'
              "
              >Download ZIP
            </b-button>
            <b-button v-b-modal.delete-modal variant="danger" size="sm"
              >Delete
            </b-button>
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
import CharacterGroupingSelect from '../Menus/CharacterGroupingSelect'
import NewCharacterGrouping from '../CharacterGroups/NewCharacterGrouping'
import CharacterImage from '../Characters/CharacterImage'
import CharacterList from '../Characters/CharacterList'
import { HTTP } from '../../main'
import moment from 'moment'
import _ from 'lodash'

export default {
  name: 'CharacterGroupingInterface',
  components: {
    CharacterGroupingSelect,
    NewCharacterGrouping,
    CharacterImage,
    CharacterList,
  },
  props: {},
  data() {
    return {
      cg_id: null,
      selected_cg: null,
      displayed_images: [],
      new_cg_card: {
        show: false,
        button_variant: {
          false: 'primary',
          true: 'warning',
        },
        button_text: {
          false: 'New',
          true: 'Cancel',
        },
      },
      cg_menu_key: 0,
      book: null,
      character_class: null,
      character_run: null,
      char_agreement: 'all',
      order: 'character_class',
      show_damaged_characters: false,
      page_start: null,
      page_end: null,
    }
  },
  computed: {
    intersecting_images: function () {
      if (!!this.selected_cg & !!this.displayed_images) {
        var cg_ids = this.selected_cg.characters.map((c) => c.id)
        var ls_ids = this.displayed_images.map((c) => c.id)
        return _.intersection(cg_ids, ls_ids)
      } else {
        return []
      }
    },
    selected_cg_ordered_chars: function () {
      if (!!this.selected_cg) {
        return _.orderBy(
          this.selected_cg.characters,
          [(character) => character.character_class.toLowerCase()],
          ['asc']
        )
      }
      return []
    },
    view_params() {
      return {
        book: this.book,
        order: this.order,
        character_run: this.character_run,
        character_class: this.character_class,
        char_agreement: this.char_agreement,
        show_damaged_characters: this.show_damaged_characters,
        ...(this.page_start && { page_start: this.page_start }),
        ...(this.page_end && { page_end: this.page_end }),
      }
    },
  },
  asyncComputed: {
    selected_cg: {
      get() {
        if (!!this.cg_id) {
          return HTTP.get('/character_groupings/' + this.cg_id + '/').then(
            (response) => {
              return response.data
            },
            (error) => {
              console.log(error)
            }
          )
        }
      },
    },
  },
  methods: {
    display_date: function (date) {
      return moment(new Date(date)).format('MM-DD-YY, h:mm a')
    },
    register_character: function (char_id) {
      if (!!this.cg_id) {
        // Send the add request to the endpoint
        return HTTP.patch(
          '/character_groupings/' + this.cg_id + '/add_characters/',
          { characters: [char_id] }
        ).then(
          (response) => {
            console.log(response)
            this.$asyncComputed.selected_cg.update()
          },
          (error) => {
            console.log(error)
          }
        )
      }
    },
    deregister_character: function (char_id) {
      if (!!this.cg_id) {
        // Send the add request to the endpoint
        return HTTP.patch(
          '/character_groupings/' + this.cg_id + '/delete_characters/',
          { characters: [char_id] }
        ).then(
          (response) => {
            console.log(response)
            this.$asyncComputed.selected_cg.update()
          },
          (error) => {
            console.log(error)
          }
        )
      }
    },
    toggle_create: function () {
      this.new_cg_card.show = !this.new_cg_card.show
    },
    create_group: function (obj) {
      this.new_cg_card.show = false
      const payload = {
        label: obj.label,
        notes: obj.notes,
        characters: [],
      }
      return HTTP.post('/character_groupings/', payload).then(
        (response) => {
          this.refresh_cg_menu()
          this.cg_id = response.data.id
        },
        (error) => {
          console.log(error)
        }
      )
    },
    delete_group: function () {
      return HTTP.delete(
        '/character_groupings/' + this.selected_cg.id + '/'
      ).then(
        (response) => {
          console.log(response)
          this.refresh_cg_menu()
          this.cg_id = null
          this.selected_cg = null
        },
        (error) => {
          console.log(error)
        }
      )
    },
    edit_group: function (id, field, content) {
      var payload = {}
      payload[field] = content
      return HTTP.patch('/character_groupings/' + id + '/', payload).then(
        (response) => {
          this.refresh_cg_menu()
          this.cg_id = response.data.id
        },
        (error) => {
          console.log(error)
        }
      )
    },
    refresh_cg_menu: function () {
      this.cg_menu_key += 1
    },
    update_page_range(page_range) {
      this.page_start = Number(page_range[0])
      this.page_end = Number(page_range[1])
    },
  },
  created() {
    this.book = this.$route.query.book
    this.order = this.$route.query.order
    this.character_run = this.$route.query.character_run
    this.character_class = this.$route.query.character_class
    this.char_agreement = this.$route.query.char_agreement
    this.show_damaged_characters =
      this.$route.query.show_damaged_characters === 'true'
    this.page_start = !!this.$route.query.page_start
      ? Number(this.$route.query.page_start)
      : null
    this.page_end = !!this.$route.query.page_end
      ? Number(this.$route.query.page_end)
      : null
  },
  updated() {
    this.$router.push({
      name: 'CharacterGroupingView',
      query: this.view_params,
    })
  },
}
</script>
