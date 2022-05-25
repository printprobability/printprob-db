<template>
    <b-container v-if="character_group" fluid class="my-3">
        <b-row>
            <b-col cols="12">
                <b-card>
                    <template v-slot:header>
                        <b-row align-h="between" class="px-3">
                            <h3>
                                {{ character_group.label }}
                            </h3>
                            <small>
                                Created by {{ character_group.created_by }} on
                                {{ display_date(character_group.date_created) }}</small>
                            <p>{{ character_group.notes }}</p>
                            <CharacterOrderingSelect v-model="order" />
                        </b-row>
                    </template>
                    <div class="d-flex flex-wrap justify-content-around" v-if="ordered_characters.length > 0">
                        <CharacterImage v-for="character in ordered_characters" :key="character.id"
                            :character="character" />
                    </div>
                    <b-alert v-else show variant="info">
                        This group has no characters yet.
                    </b-alert>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import CharacterImage from "../Characters/CharacterImage";
import CharacterOrderingSelect from "../Menus/CharacterOrderingSelect";
import { HTTP } from "../../main";
import moment from "moment";
import _ from "lodash";

export default {
    name: "CharacterGroupingDetail",
    components: {
        CharacterImage,
        CharacterOrderingSelect,
    },
    props: {
        id: String,
    },
    data() {
        return {
            order: "bookseq,pageseq,lineseq,sequence",
        }
    },
    computed: {
        ordered_characters() {
            if (this.order.variable == "bookseq,pageseq,lineseq,sequence") {
                return this.character_group.characters
            } else {
                return _.orderBy(this.character_group.characters, [this.lodash_order.variable], this.lodash_order.direction)
            }
        },
        lodash_order() {
            var direction = "asc"
            if (this.order.includes("-")) {
                direction = "desc"
            }
            const clean_string = this.order.replace("-", "")
            return {
                variable: clean_string, direction: direction
            }
        }
    },
    asyncComputed: {
        character_group() {
            return HTTP.get("/character_groupings/" + this.id + "/").then(
                (response) => {
                    return response.data;
                },
                (error) => {
                    console.log(error);
                }
            );
        }
    },
    methods: {
        display_date: function (date) {
            return moment(new Date(date)).format("MM-DD-YY, h:mm a");
        },
    },
    created: function () {
        // this.get_book(this.id);
    },
};
</script>

