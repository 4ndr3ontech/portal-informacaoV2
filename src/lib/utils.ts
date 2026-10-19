/**
 * Obtém a URL do Favicon oficial do veículo através da API pública do Google.
 */
export function getFaviconUrl(websiteUrl: string, size: number = 64): string {
  try {
    const domain = new URL(websiteUrl).hostname;
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=${size}`;
  } catch {
    return '/default-icon.svg';
  }
}

/**
 * Converte o código ISO Alpha-2 do país (ex: 'BR', 'US') na sua bandeira correspondente em Emoji.
 */
export function getCountryFlag(countryCode: string): string {
  if (!countryCode || countryCode.length !== 2) return '🌐';
  const codePoints = countryCode
    .toUpperCase()
    .split('')
    .map((char) => 127397 + char.charCodeAt(0));
  return String.fromCodePoint(...codePoints);
}

/**
 * Mapeia e retorna um ícone temático para cada categoria do portal.
 */
export function getCategoryIcon(category: string): string {
  const icons: Record<string, string> = {
    brasil: '🇧🇷',
    mundo: '🌐',
    politica: '⚖️',
    economia: '📈',
    tecnologia: '💻',
    ciencia: '🔬',
    saude: '🏥',
    esportes: '⚽',
    cultura: '🎭',
    negocios: '💼',
    'meio-ambiente': '🌿',
  };
  return icons[category.toLowerCase()] || '📰';
}