import type { APIRoute } from 'astro';

export const prerender = false;

export const GET: APIRource = async ({ request, locals }) => {
  const url = new URL(request.url);
  const secret = url.searchParams.get('token');

  if (secret !== 'meu_token_secreto_123') {
    return new Response('Acesso negado', { status: 401 });
  }

  const runtime = (locals as any).runtime;
  const db = runtime?.env?.DB;

  if (!db) {
    return new Response('Erro: Banco de dados D1 não encontrado.', { status: 500 });
  }

  try {
    const novasOfertas = [
      {
        title: 'Oferta em Destaque 1 - E-commerce / Admitad',
        description: 'Primeiro produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 89,90',
        original_price: 'R$ 129,90'
      },
      {
        title: 'Oferta em Destaque 2 - E-commerce / Admitad',
        description: 'Segundo produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 149,90',
        original_price: 'R$ 199,90'
      },
      {
        title: 'Oferta em Destaque 3 - E-commerce / Admitad',
        description: 'Terceiro produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 59,90',
        original_price: 'R$ 89,90'
      },
      {
        title: 'Oferta em Destaque 4 - E-commerce / Admitad',
        description: 'Quarto produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 199,90',
        original_price: 'R$ 259,90'
      }
    ];

    for (const oferta of novasOfertas) {
      await db.prepare(
        `INSERT INTO offers (title, description, image_url, affiliate_link, price, original_price, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)`
      ).bind(
        oferta.title, 
        oferta.description, 
        oferta.image_url, 
        oferta.affiliate_link, 
        oferta.price,
        oferta.original_price,
        new Date().toISOString()
      ).run();
    }

    // Mantém estritamente os 100 mais recentes
    await db.prepare(`
      DELETE FROM offers 
      WHERE id NOT IN (
        SELECT id FROM offers 
        ORDER BY created_at DESC, id DESC 
        LIMIT 100
      )
    `).run();

    return new Response('Sucesso: Lote de 4 ofertas inserido e limite mantido.', { status: 200 });

  } catch (error: any) {
    console.error('Erro no cron:', error);
    return new Response('Erro interno: ' + (error?.message || error), { status: 500 });
  }
};