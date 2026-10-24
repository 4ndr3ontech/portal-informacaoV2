/**
- Obtém a URL do Favicon oficial do veículo através da API pública do Google.
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
- Converte o código ISO Alpha-2 do país (ex: 'BR', 'US') em Emoji de bandeira.
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
- Retorna o ícone em emoji correspondente a cada categoria.
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
    games: '🎮',
    entretenimento: '🎬',
    educacao: '📚',
    investimentos: '💰',
  };
  return icons[category.toLowerCase()] || '📰';
}