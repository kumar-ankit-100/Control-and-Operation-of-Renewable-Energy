import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from 'tailwindcss';
import postcss from 'postcss';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: {
      plugins: [
        tailwindcss(),
        postcss(),
      ],
    },
  },
  server: {
    hmr: {
      overlay: false,
    },
  },
});
