import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import {resolve} from 'path'

export default defineConfig((mode) => {

  // const env = loadEnv(mode, process.cwd(), '')
  const OUTPUT_DIR = './_frontend/dist'
  const INPUT_DIR = './_frontend/src'

  return {
    plugins: [
      vue(),
    ],
    resolve: {
      extensions: ['.js', '.json'],
      alias: {
        '@': resolve(INPUT_DIR),
        'vue': 'vue/dist/vue.esm-bundler.js',
      },
    },
    root: resolve(INPUT_DIR),
    base: '/static/',
    server: {
      host: '0.0.0.0',
      port: 5173,
      open: false,
      watch: {
        usePolling: true,
        disableGlobbing: false,
      },
    },
    build: {
      outDir: resolve(OUTPUT_DIR),
      assetsDir: '',
      manifest: true,
      emptyOutDir: true,
      target: 'es2015',
      rollupOptions: {
        input: {
          main: resolve(`${INPUT_DIR}/js/main.js`),
        },
        output: {
          chunkFileNames: undefined,
        },
      },
    },
  }
})
