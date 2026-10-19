import type { APIRoute } from 'astro';
import { trackAffiliateClick } from '../../lib/db';

export const prerender = false;

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const body = await request.json();
    const { productId } = body;

    if (!productId) {
      return new Response(
        JSON.stringify({ success: false, message: 'ID do produto é obrigatório.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const db = locals.runtime?.env?.DB;

    if (db) {
      const userAgent = request.headers.get('user-agent') || undefined;
      const referer = request.headers.get('referer') || undefined;
      await trackAffiliateClick(db, { product_id: productId, user_agent: userAgent, referer });
    }

    return new Response(
      JSON.stringify({ success: true }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch {
    return new Response(
      JSON.stringify({ success: false, message: 'Falha ao registrar métrica.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};

export const ALL: APIRoute = async () => {
  return new Response(
    JSON.stringify({ error: 'Método não permitido.' }),
    { status: 405, headers: { 'Content-Type': 'application/json' } }
  );
};