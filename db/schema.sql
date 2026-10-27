-- Tabela para gerenciamento das Ofertas/Produtos (NOVA)
CREATE TABLE IF NOT EXISTS offers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  image_url TEXT,
  affiliate_link TEXT NOT NULL,
  price TEXT,
  is_active BOOLEAN DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para armazenamento dos envios do formulário de contato (ATUALIZADA)
CREATE TABLE IF NOT EXISTS contact_submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  subject TEXT NOT NULL,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'pendente', -- NOVO: 'pendente' ou 'respondido'
  admin_reply TEXT,               -- NOVO: Guarda a resposta enviada pelo painel
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para contabilização de acessos e cliques em ofertas de afiliados (MANTIDA)
CREATE TABLE IF NOT EXISTS affiliate_clicks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id TEXT NOT NULL,
  user_agent TEXT,
  referer TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índices de consulta otimizados para a borda (Edge)
CREATE INDEX IF NOT EXISTS idx_contact_created ON contact_submissions(created_at);
CREATE INDEX IF NOT EXISTS idx_affiliate_product ON affiliate_clicks(product_id);
CREATE INDEX IF NOT EXISTS idx_offers_active ON offers(is_active);