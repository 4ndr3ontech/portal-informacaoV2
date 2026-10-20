import { defineConfig } from 'astro/config';
<<<<<<< HEAD
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
=======

// https://astro.build/config
export default defineConfig({
  site: 'https://seusite.com.br',
  compressHTML: true,
  build: {
    format: 'directory'
  }
>>>>>>> bbd1cfd0071e0b9ddbe6684f5e8ae2ca7ace60cd
});