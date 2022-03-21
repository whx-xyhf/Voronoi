import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import * as d3 from 'd3';
import axios from './http';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Panel from './components/Panel';
import ColorPicker from './components/ColorPicker';

axios.defaults.baseURL="http://localhost:5000/";

Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.prototype.$axios=axios;
Vue.prototype.$d3=d3;
Vue.use(Panel);
Vue.use(ColorPicker);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
