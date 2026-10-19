import type { APIRoute } from 'astro';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  try {
    const db = locals.runtime?.env?.DB;

    if (!db) {
      return new Response(
        JSON.stringify({
          success: true,
          mode: 'mock',
          totals: { contacts: 0, clicks: 0 },
          contacts: [],
          clicksByProduct: []
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const contactsQuery = await db.prepare(
      `SELECT id, name, email, subject, message, created_at FROM contact_submissions ORDER BY id DESC LIMIT 20`
    ).all();

    const clicksQuery = await db.prepare(
      `SELECT product_id, COUNT(*) as total_clicks FROM affiliate_clicks GROUP BY product_id ORDER BY total_clicks DESC`
    ).all();

    const totalContacts = await db.prepare(`SELECT COUNT(*) as count FROM contact_submissions`).first<{ count: number }>();
    const totalClicks = await db.prepare(`SELECT COUNT(*) as count FROM affiliate_clicks`).first<{ count: number }>();

    return new Response(
      JSON.stringify({
        success: true,
        mode: 'live',
        totals: {
          contacts: totalContacts?.count || 0,
          clicks: totalClicks?.count || 0
        },
        contacts: contactsQuery.results || [],
        clicksByProduct: clicksQuery.results || []
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch {
    return new Response(
      JSON.stringify({ success: false, message: 'Erro ao consultar métricas.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};