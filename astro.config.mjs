import { defineConfig, passthroughImageService } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import partytown from '@astrojs/partytown';
import cloudflare from '@astrojs/cloudflare';
// Remova esta linha: import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://omundoemumclick.com.br',
  output: 'server',
  adapter: cloudflare({
    platformProxy: {
      enabled: true
    }
  }),
  image: {
    service: passthroughImageService()
  },
  integrations: [
    tailwind(), 
    partytown(),
    // Remova 'sitemap()' daqui
  ],
});