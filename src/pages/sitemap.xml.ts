import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = site ? site.toString().replace(/\/$/, '') : 'https://omundoemumclick.com.br';

  const staticPages = [
    '',
    '/noticias',
    '/ofertas',
    '/sobre',
    '/contato',
    '/privacidade',
    '/termos'
  ];

  const categoriesList = [
    'brasil',
    'mundo',
    'politica',
    'economia',
    'tecnologia',
    'ciencia',
    'saude',
    'esportes',
    'games',
    'entretenimento',
    'educacao',
    'investimentos'
  ];

  const categoryPages = categoriesList.map((slug) => `/categorias/${slug}`);
  
  // Se você tiver as fontes locais disponíveis, pode mapear aqui. 
  // Caso contrário, mantemos as rotas essenciais para garantir velocidade máxima no Cloudflare.
  const allRoutes = [...staticPages, ...categoryPages];

  const currentDate = new Date().toISOString();

  const sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${allRoutes
    .map(
      (route) => `
  <url>
    <loc>${baseUrl}${route}</loc>
    <lastmod>${currentDate}</lastmod>
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