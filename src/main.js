import Vue from 'vue'
import axios from 'axios'
import app from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
Vue.use(BootstrapVue)

Vue.config.productionTip = false
import BookList from "./components/BookList.vue";
import BookDetail from "./components/BookDetail.vue";
import PageDetail from "./components/PageDetail.vue";
import CharacterList from "./components/CharacterList.vue"

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;
export const http = axios.create({
  baseURL: "http://localhost"
})

Vue.prototype.$http = http;

const routes = [
  { path: "/books", name: "BookListView", component: BookList },
  { path: "/books/:id", name: "BookDetailView", component: BookDetail },
  { path: "/pages/:id", name: "PageDetailView", component: PageDetail },
  { path: "/characters/", name: "CharacterListView", component: CharacterList },
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

Vue.mixin({
  methods: {
    page_path: function (p, params) {
      console.log(`Getting ${p} with params: ${params}`)
      return this.$http.get(p, { params: params }).then(response => {
        console.log(`count: ${response.data.count}`)
        var response_collector = response.data.results
        if (!!response.data.next) {
          console.log(`Getting next at ${response.data.next}`)
          response_collector.concat(this.page_path(response.data.next))
        }
        return response_collector
      })
    }
  }
});

new Vue({
  router,
  render: h => h(app)
}).$mount('#app')
