export interface Env {
  DB: D1Database;
}

export default {
  // Disparado automaticamente de hora em hora pelo Cron Trigger da Cloudflare
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    ctx.waitUntil(handleAutomaticOffers(env));
  },

  // Adicionado para permitir testes manuais via navegador ou fetch localmente
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === '/test-cron') {
      await handleAutomaticOffers(env);
      return new Response('Cron executado manualmente com sucesso!', { status: 200 });
    }
    return new Response('Worker de Ofertas ativo. Acesse /test-cron para forçar a execução.', { status: 200 });
  },
};

async function handleAutomaticOffers(env: Env) {
  try {
    const novasOfertas = [
      {
        title: 'Produto Afiliado Exemplo 1',
        description: 'Descrição automática gerada pela API do Mercado Livre.',
        image_url: 'https://http2.mlstatic.com/D_NQ_NP_exemplo1.jpg',
        affiliate_link: 'https://mercadolivre.com.br/exemplo1?aff=seu_id',
        price: 'R$ 149,90'
      },
      {
        title: 'Produto Afiliado Exemplo 2',
        description: 'Descrição automática gerada pela API do Mercado Livre.',
        image_url: 'https://http2.mlstatic.com/D_NQ_NP_exemplo2.jpg',
        affiliate_link: 'https://mercadolivre.com.br/exemplo2?aff=seu_id',
        price: 'R$ 299,90'
      },
      {
        title: 'Produto Afiliado Exemplo 3',
        description: 'Descrição automática gerada pela API do Mercado Livre.',
        image_url: 'https://http2.mlstatic.com/D_NQ_NP_exemplo3.jpg',
        affiliate_link: 'https://mercadolivre.com.br/exemplo3?aff=seu_id',
        price: 'R$ 89,90'
      }
    ];

    for (const oferta of novasOfertas) {
      await env.DB.prepare(
        `INSERT INTO offers (title, description, image_url, affiliate_link, price, is_active) VALUES (?, ?, ?, ?, ?, 1)`
      ).bind(
        oferta.title, 
        oferta.description, 
        oferta.image_url, 
        oferta.affiliate_link, 
        oferta.price
      ).run();
    }

    await env.DB.prepare(`
      DELETE FROM offers 
      WHERE id NOT IN (
        SELECT id FROM offers 
        ORDER BY created_at DESC, id DESC 
        LIMIT 100
      )
    `).run();

    console.log('Sucesso: 3 novas ofertas inseridas e limite de 100 mantido.');
  } catch (error) {
    console.error('Erro ao executar a automação de ofertas:', error);
  }
}