import type { APIRoute } from 'astro';
import { categories } from '../data/categories';
import { sources } from '../data/sources';

export const GET: APIRoute = async () => {
  const baseUrl = 'https://seusite.com.br';

  const staticPages = [
    '',
    '/noticias',
    '/ofertas',
    '/sobre',
    '/contato',
    '/privacidade',
    '/termos'
  ];

  const categoryPages = categories.map((cat) => `/categorias/${cat.slug}`);
  const sourcePages = sources.map((source) => `/fontes/${source.id}`);

  const allRoutes = [...staticPages, ...categoryPages, ...sourcePages];

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${allRoutes
    .map(
      (route) => `
  <url>
    <loc>${baseUrl}${route}</loc>
    <changefreq>daily</changefreq>
    <priority>${route === '' ? '1.0' : '0.8'}</priority>
  </url>`
    )
    .join('')}
</urlset>`;

  return new Response(sitemapXml.trim(), {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8'
    }
  });
};