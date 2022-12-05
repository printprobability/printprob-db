<template>
  <b-container v-if="character_group" fluid class="my-3">
    <b-row>
      <b-col :cols="edit_mode ? 8 : 12">
        <b-card>
          <template v-slot:header>
            <b-row align-h="between" class="px-3">
              <h3>
                {{ character_group.label }}
              </h3>
              <small>
                Created by {{ character_group.created_by }} on
                {{ display_date(character_group.date_created) }}</small
              >
              <p>{{ character_group.notes }}</p>
              <CharacterOrderingSelect
                v-model="order"
                @input="order = $event"
              />
              <b-form-group
                id="sort-primary-by-book"
                label="Primary sort by book title"
                label-size="sm"
              >
                <b-form-checkbox
                  size="sm"
                  v-model="primaryBookSort"
                  name="primary-book-sort"
                >
                </b-form-checkbox>
              </b-form-group>
              <b-form-group label="Image size">
                <b-form-radio
                  v-model="image_size"
                  name="image-size"
                  value="actual"
                  >Actual pixels</b-form-radio
                >
                <b-form-radio
                  v-model="image_size"
                  name="image-size"
                  value="bound100"
                  >100px</b-form-radio
                >
                <b-form-radio
                  v-model="image_size"
                  name="image-size"
                  value="bound300"
                  >300px</b-form-radio
                >
              </b-form-group>
            </b-row>
          </template>

          <div
            class="d-flex flex-wrap justify-content-around"
            v-if="ordered_characters.length > 0"
          >
            <CharacterImage
              v-for="character in ordered_characters"
              :key="character.id"
              :character="character"
              :edit-mode="edit_mode"
              :selected="isCharSelected(character.id)"
              :image_size="image_size"
              parent-component="character_grouping_detail"
              @char_clicked="toggleCharacterSelection"
            />
          </div>
          <b-alert v-else show variant="info">
            This group has no characters yet.
          </b-alert>
        </b-card>
      </b-col>
      <b-col v-if="edit_mode" cols="4">
        <b-card>
          <template v-slot:header>
            <b-row align-h="between" class="px-3">
              <p>Move characters to another group</p>
            </b-row>
          </template>
          <div
            class="d-flex flex-wrap justify-content-around"
            v-if="ordered_characters.length > 0"
          >
            <b-button-group class="mx-1">
              <b-button @click="selectAll" variant="primary"
                >Select All</b-button
              >
              <b-button @click="deselectAll" variant="secondary"
                >Deselect All</b-button
              >
            </b-button-group>
            <b-input-group class="mx-md-auto">
              <b-row class="padded-row">
                <CharacterGroupingSelect
                  label="Select target group"
                  :excluded-character-group="this.id"
                  v-model="cg_id"
                  :hidden="showCreate"
                />
                <b-col>
                  <b-button
                    variant="success"
                    size="lg"
                    @click="addToTargetGroup"
                    :disabled="selectedCharCount === 0 || cg_id === null"
                    :hidden="showCreate"
                    >Copy To Group</b-button
                  >
                </b-col>
                <b-col>
                  <b-button
                    variant="success"
                    size="lg"
                    @click="changeGroup"
                    :disabled="selectedCharCount === 0 || cg_id === null"
                    :hidden="showCreate"
                    >Change Group</b-button
                  >
                </b-col>
              </b-row>
            </b-input-group>
          </div>
          <b-input-group class="mx-md-1">
            <b-row class="padded-row">
              <b-col>
                <b-button
                  :variant="showCreate ? 'warning' : 'success'"
                  size="lg"
                  @click="toggleCreate"
                  :disabled="selectedCharCount === 0"
                  >{{ showCreate ? 'Cancel Create' : 'Create Group' }}</b-button
                >
              </b-col>
            </b-row>
            <b-row>
              <NewCharacterGrouping
                v-show="showCreate"
                @new_group="create_new_group"
              />
            </b-row>
          </b-input-group>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import CharacterImage from '../Characters/CharacterImage'
import CharacterGroupingSelect from '../Menus/CharacterGroupingSelect'
import CharacterOrderingSelect from '../Menus/CharacterOrderingSelect'
import NewCharacterGrouping from '../CharacterGroups/NewCharacterGrouping'
import { HTTP } from '../../main'
import moment from 'moment'
import _ from 'lodash'

export default {
  name: 'CharacterGroupingDetail',
  components: {
    CharacterImage,
    CharacterOrderingSelect,
    CharacterGroupingSelect,
    NewCharacterGrouping,
  },
  props: {
    id: String,
  },
  data() {
    return {
      cg_id: null,
      order: 'character_class',
      selectedCharacters: {},
      ordered_characters: [],
      selectedCharCount: 0,
      showCreate: false,
      image_size: 'actual',
      primaryBookSort: false,
    }
  },
  computed: {
    edit_mode() {
      return !!this.$route.query.edit
    },
  },
  asyncComputed: {
    character_group() {
      return HTTP.get('/character_groupings/' + this.id + '/').then(
        (response) => {
          return response.data
        },
        (error) => {
          console.log(error)
        }
      )
    },
  },
  methods: {
    order_characters() {
      if (this.lodash_order.variable === 'bookseq,pageseq,lineseq,sequence') {
        return this.character_group.characters
      } else {
        const orderingFields = []
        const orderingDirection = []
        if (this.primaryBookSort) {
          orderingFields.push((character) =>
            character.book.label.substring(
              character.book.label.indexOf(' ') + 1
            )
          )
          orderingDirection.push('asc')
        }
        orderingFields.push(this.lodash_order.variable)
        orderingDirection.push(this.lodash_order.direction)
        return _.orderBy(
          this.character_group.characters,
          orderingFields,
          orderingDirection
        )
      }
    },
    lodash_order() {
      var direction = 'asc'
      if (this.order.includes('-')) {
        direction = 'desc'
      }
      const clean_string = this.order.replace('-', '')
      return {
        variable: clean_string,
        direction: direction,
      }
    },
    display_date: function (date) {
      return moment(new Date(date)).format('MM-DD-YY, h:mm a')
    },
    toggleCharacterSelection: function (characterId) {
      const toggleStatus = !!!this.selectedCharacters[characterId]
      this.selectedCharacters = {
        ...this.selectedCharacters,
        [characterId]: toggleStatus,
      }
      this.selectedCharCount += toggleStatus ? 1 : -1
    },
    selectAll: function () {
      const allSelected = {}
      this.ordered_characters.forEach((oc) => {
        allSelected[oc['id']] = true
      })
      this.selectedCharacters = Object.assign({}, allSelected)
      this.selectedCharCount = Object.keys(this.selectedCharacters).length
    },
    deselectAll: function () {
      const allDeselected = {}
      this.ordered_characters.forEach((oc) => {
        allDeselected[oc['id']] = false
      })
      this.selectedCharacters = Object.assign({}, allDeselected)
      this.selectedCharCount = 0
    },
    isCharSelected: function (characterId) {
      return this.selectedCharacters[characterId]
    },
    changeGroup: function () {
      return HTTP.patch(
        `/character_groupings/${this.id}/move_characters/?target_group=${this.cg_id}`,
        { characters: Object.keys(this.selectedCharacters) }
      ).then(
        (response) => {
          this.makeToast(
            'Successfully moved characters to target group!',
            'success'
          )
          console.log(response)
          this.$asyncComputed.character_group.update()
          this.selectedCharCount = 0
        },
        (error) => {
          this.makeToast(
            'Error moving characters to target group! Error: ' + error,
            'danger'
          )
          console.log(error)
        }
      )
    },
    makeToast(body, variant) {
      this.$bvToast.toast(body, {
        title: variant === 'danger' ? 'Error!' : 'Success',
        variant: variant,
        solid: true,
        autoHideDelay: 3000,
      })
    },
    addToTargetGroup: function () {
      return HTTP.patch(`/character_groupings/${this.cg_id}/add_characters/`, {
        characters: Object.keys(this.selectedCharacters),
      }).then(
        (response) => {
          this.makeToast(
            'Successfully added characters to target group!',
            'success'
          )
          console.log(response)
          this.selectedCharCount = 0
        },
        (error) => {
          this.makeToast(
            'Error adding characters to target group! Error: ' + error,
            'danger'
          )
          console.log(error)
        }
      )
    },
    toggleCreate: function () {
      this.showCreate = !this.showCreate
    },
    create_new_group: function (obj) {
      this.showCreate = false
      const payload = {
        label: obj.label,
        notes: obj.notes,
        characters: Object.keys(this.selectedCharacters),
      }
      return HTTP.post('/character_groupings/', payload).then(
        (response) => {
          this.makeToast('Successfully created new group!', 'success')
          console.log(response)
          this.selectedCharCount = 0
        },
        (error) => {
          this.makeToast('Error creating new group! Error: ' + error, 'danger')
          console.log(error)
        }
      )
    },
  },
  watch: {
    order: function () {
      this.ordered_characters = this.order_characters()
    },
    primaryBookSort: function () {
      this.ordered_characters = this.order_characters()
    },
    character_group: function (val) {
      if (val) {
        this.ordered_characters = this.order_characters()
      }
    },
  },
}
</script>

<style scoped>
.padded-row {
  padding: 5px;
}
</style>
