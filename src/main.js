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

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;


const routes = [
  { path: "/books", name: "BookListView", component: BookList },
  { path: "/books/:id", name: "BookDetailView", component: BookDetail },
  { path: "/pages/:id", name: "PageDetailView", component: PageDetail }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

new Vue({
  router,
  render: h => h(app)
}).$mount('#app')
