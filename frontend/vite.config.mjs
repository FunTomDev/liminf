import { defineConfig } from 'vite'
import { resolve } from 'path'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    root: '.',
    base: '/static/',
    plugins: [
      tailwindcss(),
    ],
    server: {
        origin: 'http://localhost:5173',
        cors: true,
    },
    build: {
        manifest: "manifest.json",
        outDir: resolve("./assets"),
        rollupOptions: {
            input: {
                main: resolve('./src/main.js'),
                milkdown: resolve('./src/js/milkdown-setup.js'),
                carousel_main: resolve('./src/js/carousel-main.js'),
                carousel_profile: resolve('./src/js/carousel-profile.js'),
                dropdown: resolve('./src/js/custom-dropdown.js'),
                filter_toggle: resolve('./src/js/filter-toggle.js'),
                menu_toggle: resolve('./src/js/menu-toggle.js'),
                tilter: resolve('./src/js/tilter.js'),
            }
        }
    },
})