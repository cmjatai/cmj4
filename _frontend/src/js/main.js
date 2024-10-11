import 'vite/modulepreload-polyfill'
import '../css/styles.css'

import { createApp } from 'vue'

import App from './App.vue'

const app = createApp(App)

app.mount("#app")