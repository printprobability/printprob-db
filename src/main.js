import Vue from 'vue'
import app from './App.vue'
import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
Vue.use(BootstrapVue)

Vue.config.productionTip = false
import Home from "./components/Home"
import BookList from "./components/Books/BookList";
import BookDetail from "./components/Books/BookDetail";
import CharacterGroupingInterface from "./components/Interfaces/CharacterGroupingInterface";
import CharacterReviewInterface from "./components/Interfaces/CharacterReviewInterface";

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "xsrfcookie";
axios.defaults.withCredentials = true;

export const HTTP = axios.create({
  baseURL: process.env.VUE_APP_PP_ENDPOINT
})

Vue.prototype.$APIConstants = {
  REST_PAGE_SIZE: 100,
  API_LOGIN: "/api/auth/login/?next=/",
  API_LOGOUT: "/api/auth/logout/?next=/"
}

const routes = [
  { path: "/", name: "HomeView", component: Home },
  { path: "/books", name: "BookListView", component: BookList },
  {
    path: "/books/:id", name: "BookDetailView", component: BookDetail, props: (route) => ({ id: Number(route.params.id) })
  },
  {
    path: "/group_characters", name: "CharacterGroupingView", component: CharacterGroupingInterface, props: (route) => ({
      page: (!!route.query.page) ? Number(route.query.page) : 1,
      character_class: route.query.character_class,
      book: (!!route.query.book) ? Number(route.query.book) : null,
      order: route.query.order,
      character_run: route.query.character_run
    })
  },
  { path: "/character_review", name: "CharacterReviewView", component: CharacterReviewInterface }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

new Vue({
  router,
  render: h => h(app)
}).$mount('#app')
