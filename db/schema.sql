export interface Env {
  DB: D1Database;
}

export default {
  // Disparado automaticamente de hora em hora pelo Cron Trigger da Cloudflare
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    ctx.waitUntil(handleAutomaticOffers(env));
  },
};

async function handleAutomaticOffers(env: Env) {
  try {
    // 1. Simulação ou requisição à API de afiliados (Ex: Mercado Livre)
    // Aqui você fará o seu fetch para coletar até 3 ofertas novas
    const novasOfertas = [
      {
        title: 'Produto Exemplo Afiliado 1',
        description: 'Descrição detalhada do produto em promoção.',
        image_url: 'https://http2.mlstatic.com/D_NQ_NP_exemplo1.jpg',
        affiliate_link: 'https://mercadolivre.com.br/exemplo1?aff=seu_id',
        price: 'R$ 199,90'
      },
      // ... adicione as outras ofertas extraídas
    ];

    for (const oferta of novasOfertas) {
      // Insere a nova oferta na tabela 'offers'
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

    // 2. Regra para manter apenas as 100 ofertas mais recentes (deleta o excedente antigo)
    await env.DB.prepare(`
      DELETE FROM offers 
      WHERE id NOT IN (
        SELECT id FROM offers 
        ORDER BY created_at DESC, id DESC 
        LIMIT 100
      )
    `).run();

    console.log('Automação de ofertas concluída: 3 inseridas e limite de 100 mantido.');
  } catch (error) {
    console.error('Erro na automação de ofertas:', error);
  }
}