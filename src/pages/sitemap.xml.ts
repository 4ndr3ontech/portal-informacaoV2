import type { APIRoute } from 'astro';
import fontesGlobaisJson from '../data/clean-news-sources.json';
import { sources as fontesBrasil } from '../data/sources';

export const prerender = true;

export const GET: APIRoute = async () => {
  const domain = 'https://www.omundoemumclick.com.br';
  
  const staticPages = [
    '',
    '/noticias',
    '/ofertas',
    '/sobre',
    '/contato',
    '/privacidade',
    '/termos',
    '/metodologia'
  ];

  const categories = [
    'brasil',
    'mundo',
    'politica',
    'economia',
    'tecnologia',
    'games',
    'esportes',
    'ciencia',
    'saude'
  ];

  // Normaliza e unifica as fontes globais e brasileiras
  const fontesGlobais = Array.isArray(fontesGlobaisJson)
    ? fontesGlobaisJson
    : ((fontesGlobaisJson as any)?.default || []);

  const rawAllSources = [...fontesGlobais, ...fontesBrasil];
  const allSources = Array.from(
    new Map(
      rawAllSources
        .filter(source => source && source.id)
        .map(source => [source.id, source])
    ).values()
  );

  const currentDate = new Date().toISOString().split('T')[0];

  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

  // Páginas estáticas principais
  staticPages.forEach(page => {
    xml += `  <url>\n`;
    xml += `    <loc>${domain}${page}</loc>\n`;
    xml += `    <lastmod>${currentDate}</lastmod>\n`;
    xml += `    <changefreq>daily</changefreq>\n`;
    xml += `    <priority>${page === '' ? '1.0' : '0.8'}</priority>\n`;
    xml += `  </url>\n`;
  });

  // Categorias (usando o parâmetro de busca por categoria da sua aplicação)
  categories.forEach(cat => {
    xml += `  <url>\n`;
    xml += `    <loc>${domain}/noticias?category=${cat}</loc>\n`;
    xml += `    <lastmod>${currentDate}</lastmod>\n`;
    xml += `    <changefreq>daily</changefreq>\n`;
    xml += `    <priority>0.8</priority>\n`;
    xml += `  </url>\n`;
  });

  // Fontes individuais cadastradas no diretório
  allSources.forEach((source: any) => {
    const slug = source.slug || source.id;
    if (slug) {
      xml += `  <url>\n`;
      xml += `    <loc>${domain}/fontes/${slug}</loc>\n`;
      xml += `    <lastmod>${currentDate}</lastmod>\n`;
      xml += `    <changefreq>weekly</changefreq>\n`;
      xml += `    <priority>0.6</priority>\n`;
      xml += `  </url>\n`;
    }
  });

  xml += `</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8'
    }
  });
};