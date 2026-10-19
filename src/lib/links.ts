/**
 * Sanitiza e valida URLs externas para evitar esquemas inválidos ou injeções.
 */
export function sanitizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      return '#';
    }
    return parsed.toString();
  } catch {
    return '#';
  }
}

/**
 * Atributos padrão de segurança para links externos editoriais.
 */
export function getExternalLinkProps() {
  return {
    target: '_blank',
    rel: 'noopener noreferrer'
  };
}

/**
 * Atributos recomendados para links comerciais e de afiliados (SEO + Rastreamento).
 */
export function getAffiliateLinkProps() {
  return {
    target: '_blank',
    rel: 'nofollow sponsored noopener noreferrer'
  };
}