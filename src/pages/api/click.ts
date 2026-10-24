import type { APIRoute } from 'astro';

// Informa ao Astro para não tentar pré-renderizar esta rota na build estática
export const prerender = false;

// Exemplo simples em memória ou integração com seu DB (Prisma, KV, Supabase, PostgreSQL, etc.)
// Substitua o objeto/banco de dados abaixo pela sua camada de persistência real.
export const clickStore: Record<string, number> = {
  'bbc-news-brasil': 1420,
  'g1': 980,
  'uol-noticias': 850
};

export const POST: APIRoute = async ({ request }) => {
  try {
    const { sourceId } = await request.json();

    if (!sourceId) {
      return new Response(JSON.stringify({ error: 'ID da fonte ausente' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Incrementa o contador do veículo
    clickStore[sourceId] = (clickStore[sourceId] || 0) + 1;

    return new Response(
      JSON.stringify({ success: true, clicks: clickStore[sourceId] }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Erro ao registrar clique' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};