import { defineConfig, passthroughImageService } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import partytown from '@astrojs/partytown';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  site: 'https://omundoemumclick.com.br',
  output: 'server',
  adapter: cloudflare({
    platformProxy: {
      enabled: true
    }
  }),
  image: {
    service: passthroughImageService() // Resolve o aviso do Sharp na Cloudflare
  },
  integrations: [
    tailwind(), 
    partytown()
  ],
});