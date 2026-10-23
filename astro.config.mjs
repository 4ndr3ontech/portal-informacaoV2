import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import partytown from '@astrojs/partytown';

export default defineConfig({
  site: 'https://omundoemumclick.com.br',
  integrations: [tailwind(), partytown()],
});