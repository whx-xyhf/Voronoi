import Vue from 'vue'
import VueRouter from 'vue-router'
import __Main from '../views/__Main'
import Main from "../views/Main.vue"
import Upload from "../components/Sidebar/upload.vue"

Vue.use(VueRouter)

const routes = [
  {
    path:'/',
    name:'Main',
    component:Main,
    children: [
      {
        path: "/upload",
        name: "upload",
        component: Upload,
      }
    ]
  },
  {
    path: "/__",
    name: '__main',
    component: __Main,
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
