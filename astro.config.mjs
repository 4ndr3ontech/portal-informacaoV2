import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://seusite.com.br',
  compressHTML: true,
  build: {
    format: 'directory'
  },
  integrations: [tailwind()],
});