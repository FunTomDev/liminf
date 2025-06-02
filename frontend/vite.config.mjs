import { defineConfig } from 'vite'
import { resolve } from 'path'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    root: '.',  // keep it relative to frontend/
    plugins: [
      tailwindcss(),
    ],
    build: {
        outDir: './dist/',
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                main: resolve('src/main.js'),
            },
        },
    },
})