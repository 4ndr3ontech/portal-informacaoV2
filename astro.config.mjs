import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import partytown from '@astrojs/partytown';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://omundoemumclick.com.br',
  integrations: [tailwind(), partytown(), sitemap()],
});