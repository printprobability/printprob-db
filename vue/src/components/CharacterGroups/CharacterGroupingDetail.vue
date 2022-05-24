<template>
    <b-container v-if="character_group" fluid class="my-3">
        <b-row>
            <b-col cols="12">
                <b-card>
                    <template v-slot:header>
                        <b-row align-h="between" class="px-3">
                            {{ character_group.label }}
                            <small>
                                Created by {{ character_group.created_by }} on
                                {{ display_date(character_group.date_created) }}</small>
                            <CharacterOrderingSelect :value="order" @input="$emit('order_input', $event)" />
                        </b-row>
                    </template>
                    <div class="d-flex flex-wrap justify-content-around" v-if="character_group.characters.length > 0">
                        <CharacterImage v-for="character in character_group.characters" :key="character.id"
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
            order: "-class_probability",
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

