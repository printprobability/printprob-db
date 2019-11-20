import Vue from 'vue'
import app from './App.vue'
import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueRouter from 'vue-router'
import AsyncComputed from 'vue-async-computed'

Vue.use(VueRouter)
Vue.use(BootstrapVue)
Vue.use(AsyncComputed)

Vue.config.productionTip = false
import Home from "./components/Home"
import BookList from "./components/Books/BookList";
import BookDetail from "./components/Books/BookDetail";
import BookCreate from "./components/Books/BookCreate";
import CharacterGroupingInterface from "./components/Interfaces/CharacterGroupingInterface";
import CharacterReviewInterface from "./components/Interfaces/CharacterReviewInterface";
import SpreadDetail from "./components/Spreads/SpreadDetail";
import CharacterDetail from "./components/Characters/CharacterDetail"

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "xsrfcookie";
axios.defaults.withCredentials = true;

Vue.prototype.$APIConstants = {
  REST_PAGE_SIZE: 100,
  BOOK_PAGE_SIZE: 25,
  API_LOGIN: "/api/auth/login/?next=/",
  API_LOGOUT: "/api/auth/logout/?next=/",
  PP_ENDPOINT: process.env.VUE_APP_PP_ENDPOINT
}

export const HTTP = axios.create({
  baseURL: process.env.VUE_APP_PP_ENDPOINT
})


const routes = [
  { path: "/", name: "HomeView", component: Home },
  { path: "/books", name: "BookListView", component: BookList },
  {
    path: "/books/:id", name: "BookDetailView", component: BookDetail, props: (route) => ({ id: route.params.id })
  },
  {
    path: "/create/book", name: "BookCreateView", component: BookCreate
  },
  {
    path: "/spreads/:id", name: "SpreadDetailView", component: SpreadDetail, props: (route) => ({ id: route.params.id })
  },
  {
    path: "/characters/:id", name: "CharacterDetailView", component: CharacterDetail, props: (route) => ({ id: route.params.id })
  },
  {
    path: "/group_characters", name: "CharacterGroupingView", component: CharacterGroupingInterface, props: (route) => ({
      page: (!!route.query.page) ? Number(route.query.page) : 1,
      character_class: route.query.character_class,
      book: (!!route.query.book) ? route.query.book : null,
      order: route.query.order,
      character_run: route.query.character_run
    })
  },
  {
    path: "/character_review", name: "CharacterReviewView", component: CharacterReviewInterface, props: (route) => ({
      page: (!!route.query.page) ? Number(route.query.page) : 1,
      character_class: route.query.character_class,
      book: (!!route.query.book) ? route.query.book : null,
      order: route.query.order,
      character_run: route.query.character_run
    })
  }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

new Vue({
  router,
  render: h => h(app)
}).$mount('#app')
