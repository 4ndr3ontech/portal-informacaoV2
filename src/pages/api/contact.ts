import type { APIRoute } from 'astro';
import { validateContactForm } from '../../lib/validation';
import { saveContactSubmission } from '../../lib/db';

export const prerender = false;

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const data = await request.json();
    const validation = validateContactForm(data);

    if (!validation.isValid) {
      return new Response(
        JSON.stringify({ success: false, errors: validation.errors }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const db = locals.runtime?.env?.DB;

    if (db) {
      await saveContactSubmission(db, data);
    } else {
      console.warn('Banco D1 não disponível neste ambiente local/build.');
    }

    return new Response(
      JSON.stringify({ success: true, message: 'Mensagem recebida e registrada com sucesso!' }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch {
    return new Response(
      JSON.stringify({ success: false, message: 'Erro ao processar a requisição.' }),
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