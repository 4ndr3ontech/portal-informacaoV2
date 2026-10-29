import type { APIRoute } from 'astro';

export const prerender = false;

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const secret = url.searchParams.get('token');

  // Proteção por token secreto validado pelo cron-job.org
  if (secret !== 'meu_token_secreto_123') {
    return new Response('Acesso negado', { status: 401 });
  }

  const runtime = (locals as any).runtime;
  const db = runtime?.env?.DB;

  if (!db) {
    return new Response('Erro: Banco de dados D1 não encontrado no ambiente.', { status: 500 });
  }

  try {
    // Aqui simulamos ou puxamos os novos produtos da Admitad / Lojas parceiras
    // Nas próximas etapas, podemos ligar diretamente à API de produtos da Admitad.
    const novasOfertas = [
      {
        title: 'Oferta em Destaque - Admitad / E-commerce',
        description: 'Produto selecionado automaticamente via automação.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 99,90',
        original_price: 'R$ 149,90'
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

    // Regra de Ouro: Mantém apenas os 100 produtos mais recentes e remove os antigos
    await db.prepare(`
      DELETE FROM offers 
      WHERE id NOT IN (
        SELECT id FROM offers 
        ORDER BY created_at DESC, id DESC 
        LIMIT 100
      )
    `).run();

    return new Response(JSON.stringify({ success: true, message: 'Cron executado com sucesso! Ofertas atualizadas e limite de 100 mantido.' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error: any) {
    console.error('Erro na automação do cron:', error);
    return new Response(JSON.stringify({ error: error.message || 'Erro interno no servidor' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};