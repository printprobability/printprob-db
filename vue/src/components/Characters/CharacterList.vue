<template>
<div id="charlist">
    <div class="card">
        <div class="card-header">Filter Characters</div>
        <div class="card-body">
            <div class="row">
                <div class="col-4">
                    <CharacterClassSelect :multiple="true" :values="character_class" @input="$emit('character_class_input', $event)" />
                </div>
                <div class="col-8">
                    <p v-if="!!book">
                        <b-button @click="clear_book" variant="danger" size="sm">x
                        </b-button>
                        <strong>Book:</strong>
                        {{ book_title }}
                    </p>
                    <div v-else>
                        <BookAutocomplete :value="book" @input="$emit('book_input', $event)" />
                    </div>
                </div>
            </div>
            <b-row>
                <div class="col-4">
                    <CharacterAgreementRadio :value="char_agreement" @input="$emit('char_agreement_input', $event)" />
                </div>
                <div class="col-4">
                    <CharacterOrderingSelect :value="order" @input="$emit('order_input', $event)" />
                </div>
                <div class="col-4" v-if="!!!book">
                    <ShowDamagedCharactersCheckbox :value="show_damaged_characters" @input="$emit('damaged_characters_input', $event)" />
                </div>
            </b-row>
            <b-row v-if="!!book">
                <div class="col-6">
                    <PageRangeInput :page_start="page_start" :page_end="page_end" @input="$emit('page_range_input', $event)" />
                </div>
                <div class="col-6">
                    <ShowDamagedCharactersCheckbox :value="show_damaged_characters" @input="$emit('damaged_characters_input', $event)" />
                </div>
            </b-row>
        </div>
    </div>
    <div class="char-images card my-2">
        <div class="card-header">
            <Spinner v-if="progress_spinner" />
            <div class="paginator" v-if="value.length > 0">
                <p>
                    Characters {{ 1 + (page - 1) * $APIConstants.REST_PAGE_SIZE }} to
                    {{ (page - 1) * $APIConstants.REST_PAGE_SIZE + value.length }}
                    <span v-if="characters.next" v-b-tooltip.hover title="Arbitrarily counting characters is a very expensive operation, so we only estimate here...">(out of many)</span>
                </p>
                <b-pagination hide-goto-end-buttons v-show="pagination_needed" v-model="page" :per-page="$APIConstants.REST_PAGE_SIZE" :total-rows="mock_rows" aria-controls="character-results" limit="3" />
                <b-form-group label="Image size">
                    <b-form-radio v-model="image_size" name="image-size" value="actual">Actual pixels
                    </b-form-radio>
                    <b-form-radio v-model="image_size" name="image-size" value="bound100">100px
                    </b-form-radio>
                    <b-form-radio v-model="image_size" name="image-size" value="bound300">300px
                    </b-form-radio>
                </b-form-group>
            </div>
            <div show v-else>No matching characters</div>
        </div>
        <div class="d-flex flex-wrap card-body" id="character-results" v-if="value.length > 0">
            <CharacterImage v-for="character in value" :character="character" :key="character.id" :highlight="highlighted_characters.includes(character.id)" :bad="bad_characters.includes(character.id)" :good="good_characters.includes(character.id)" :image_size="image_size" parent-component="character_list" @char_clicked="$emit('char_clicked', $event)" />
        </div>
    </div>
</div>
</template>

<script>
import ShowDamagedCharactersCheckbox from '../Menus/ShowDamagedCharactersCheckbox'
import CharacterClassSelect from '../Menus/CharacterClassSelect'
import CharacterOrderingSelect from '../Menus/CharacterOrderingSelect'
import BookAutocomplete from '../Menus/BookAutocomplete'
import CharacterAgreementRadio from '../Menus/CharacterAgreementRadio'
import PageRangeInput from '../Menus/PageRangeInput'
import CharacterImage from './CharacterImage'
import Spinner from '../Interfaces/Spinner'
import {
    HTTP
} from '../../main'
import axios from 'axios'
import {
    debounce
} from 'lodash'

export default {
    
    name: 'CharacterList',
    props: {
        highlighted_characters: {
            type: Array,
            default: function () {
                return []
            },
        },
        bad_characters: {
            type: Array,
            default: function () {
                return []
            },
        },
        good_characters: {
            type: Array,
            default: function () {
                return []
            },
        },
        character_class: {
            default: () => [],
            type: Array,
        },
        book: {
            default: null,
            type: String,
        },
        char_agreement: {
            default: 'all',
            type: String,
        },
        order: {
            default: 'character_class',
            type: String,
        },
        show_damaged_characters: {
            type: Boolean,
            default: true,
        },
        value: {
            // Here is where the characters themselves live
            type: Array,
            default: () => [],
        },
        input_page_start: {
            type: Number,
            default: null,
        },
        input_page_end: {
            type: Number,
            default: null,
        },
        character_run: {
            default: "",
            type: String
        },
    },
    components: {
        ShowDamagedCharactersCheckbox,
        PageRangeInput,
        CharacterClassSelect,
        CharacterOrderingSelect,
        BookAutocomplete,
        CharacterAgreementRadio,
        CharacterImage,
        Spinner,
    },
    data() {
        return {
            progress_spinner: false,
            cursor: null,
            image_size: 'actual',
            previous_requests: [],
            characters: {
                results: [],
                next: null,
                prev: null
            },
            page: 1,
            page_start: this.input_page_start,
            page_end: this.input_page_end,
        }
    },
    asyncComputed: {
        results() {
            if (!!!this.book) {
                return
            }
            // cancel all previous requests
            this.previous_requests.forEach((request) => {
                request.cancel('Cancelling in favor of new fetch')
            })
            this.previous_requests = []
            const payload = {
                limit: this.$APIConstants.REST_PAGE_SIZE,
                offset: this.rest_offset,
                character_class: this.character_class,
                character_run: this.character_run,
                book: this.book,
                agreement: this.char_agreement,
                ordering: this.order,
                ...(this.input_page_start && {
                    page_sequence_gte: this.input_page_start,
                }),
                ...(this.input_page_end && {
                    page_sequence_lte: this.input_page_end
                }),
                ...(this.show_damaged_characters && {
                    damage_score_gte: 0.0
                }),
            }
            // debounced call - we don't want this to trigger too many times
            return this.getCharacters(payload)
        },
        book_title() {
            if (!!this.book) {
                return HTTP.get('/books/' + this.book + '/').then(
                    (response) => {
                        return response.data.label
                    },
                    (error) => {
                        console.log(error)
                    }
                )
            }
        },
    },
    computed: {
        view_params() {
            return {
                limit: this.$APIConstants.REST_PAGE_SIZE,
                character_class: this.character_class,
                character_run: this.character_run,
                book: this.book,
                agreement: this.char_agreement,
                order: this.order,
                cursor: this.cursor,
                show_damaged_characters: this.show_damaged_characters,
                page_start: this.page_start,
                page_end: this.page_end,
            }
        },
        rest_offset: function () {
            return (this.page - 1) * this.$APIConstants.REST_PAGE_SIZE
        },
        pagination_needed: function () {
            return !!this.characters.next || !!this.characters.previous
        },
        mock_rows: function () {
            var baseline = this.rest_offset + this.value.length
            if (!!this.characters.next) {
                baseline += this.$APIConstants.REST_PAGE_SIZE
            }
            return baseline
        },
    },
    methods: {
        clear_book() {
            this.$emit('book_input', null)
        },
        getCharacters: debounce(function (payload) {
            const request = axios.CancelToken.source()
            this.previous_requests.push(request)
            this.progress_spinner = true

            return HTTP.get('/characters/', {
                    params: payload,
                    cancelToken: request.token,
                    paramsSerializer: {
                        indexes: null
                    }
                })
                .then(
                    (response) => {
                        this.characters = response.data
                    },
                    (error) => {
                        console.log(error)
                    }
                )
                .finally(() => {
                    this.progress_spinner = false
                })
        }, 250),
    },
    watch: {
        characters() {
            this.$emit('input', this.characters.results)
        },
        view_params() {
            this.page = 1
        },
    },
}
</script>
