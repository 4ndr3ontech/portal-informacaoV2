import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request, locals }) => {
  const url = new URL(request.url);
  const secret = url.searchParams.get('token');

  // Proteção básica para que apenas você (ou o robô) possa disparar o script
  if (secret !== 'meu_token_secreto_123') {
    return new Response('Acesso negado', { status: 401 });
  }

  // Acessar o banco D1 através do ambiente runtime do Astro (Cloudflare)
  const db = locals.runtime.env.DB;

  try {
    const novasOfertas = [
      {
        title: 'Produto Afiliado Exemplo - Produção 1',
        description: 'Descrição automática gerada pela API.',
        image_url: 'https://http2.mlstatic.com/D_NQ_NP_exemplo1.jpg',
        affiliate_link: 'https://mercadolivre.com.br/exemplo1?aff=seu_id',
        price: 'R$ 149,90'
      },
      // Pode adicionar mais dados de teste aqui se quiser
    ];

    for (const oferta of novasOfertas) {
      await db.prepare(
        `INSERT INTO offers (title, description, image_url, affiliate_link, price, is_active) VALUES (?, ?, ?, ?, ?, 1)`
      ).bind(
        oferta.title, 
        oferta.description, 
        oferta.image_url, 
        oferta.affiliate_link, 
        oferta.price
      ).run();
    }

    await db.prepare(`
      DELETE FROM offers 
      WHERE id NOT IN (
        SELECT id FROM offers 
        ORDER BY created_at DESC, id DESC 
        LIMIT 100
      )
    `).run();

    return new Response('Sucesso: Ofertas inseridas e limite mantido.', { status: 200 });
  } catch (error: any) {
    console.error(error);
    return new Response('Erro na automação: ' + error.message, { status: 500 });
  }
};