export interface ContactRecord {
  id?: number;
  name: string;
  email: string;
  subject: string;
  message: string;
  created_at?: string;
}

export interface AffiliateClickRecord {
  id?: number;
  product_id: string;
  user_agent?: string;
  referer?: string;
  created_at?: string;
}

/**
 * Insere um registro de contato no banco de dados Cloudflare D1.
 */
export async function saveContactSubmission(db: D1Database, record: ContactRecord) {
  const stmt = db.prepare(
    `INSERT INTO contact_submissions (name, email, subject, message) VALUES (?, ?, ?, ?)`
  );
  return await stmt.bind(record.name, record.email, record.subject, record.message).run();
}

/**
 * Registra um evento de clique em oferta de afiliado no D1.
 */
export async function trackAffiliateClick(db: D1Database, record: AffiliateClickRecord) {
  const stmt = db.prepare(
    `INSERT INTO affiliate_clicks (product_id, user_agent, referer) VALUES (?, ?, ?)`
  );
  return await stmt.bind(record.product_id, record.user_agent || null, record.referer || null).run();
}