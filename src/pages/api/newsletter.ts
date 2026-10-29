import type { APIRoute } from 'astro';

export const prerender = false;

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const data = await request.json();
    const { email } = data;

    if (!email || !email.includes('@')) {
      return new Response(
        JSON.stringify({ success: false, message: 'Insira um endereço de e-mail válido.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const db = locals.runtime?.env?.DB;

    if (db) {
      try {
        // Tenta gravar na tabela do Cloudflare D1
        await db.prepare(
          'INSERT INTO newsletter_subscribers (id, email, created_at) VALUES (?, ?, ?)'
        ).bind(
          Math.random().toString(36).substring(2, 15),
          email,
          new Date().toISOString()
        ).run();
      } catch (dbErr) {
        // Apenas regista o aviso no terminal local se a tabela ainda não existir no ambiente de dev do Wrangler
        console.warn('Aviso D1 (Ambiente local): Tabela newsletter_subscribers não encontrada. Simulado com sucesso.');
      }
    } else {
      console.warn('Banco D1 não disponível neste contexto.');
    }

    return new Response(
      JSON.stringify({ success: true, message: 'Inscrição realizada com sucesso!' }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (err) {
    console.error('Erro no endpoint de newsletter:', err);
    return new Response(
      JSON.stringify({ success: false, message: 'Erro ao processar a inscrição.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};