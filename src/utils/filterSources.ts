import { sources as fontesOriginais } from '../data/sources';
import type { NewsSource, Category } from '../types';

// Converte de forma segura passando por unknown para alinhar as propriedades (ex: score)
const catalog: NewsSource[] = (fontesOriginais as unknown) as NewsSource[];

/**
 * Retorna todas as fontes unificadas e ativas do diretório.
 */
export function getAllSources(): NewsSource[] {
  return catalog.filter(source => source.active !== false);
}

/**
 * Filtra o catálogo unificado por um nicho específico, retornando apenas fontes ativas.
 * Adicionado fallback `|| 999` para evitar erro de null/undefined no rank.
 */
export function getSourcesByCategory(category: string | Category): NewsSource[] {
  const catLower = String(category).toLowerCase().trim();

  return catalog
    .filter(source => {
      if (source.active === false) return false;

      // Se a categoria solicitada for 'brasil', traz todas as fontes do país BR
      if (catLower === 'brasil') {
        return source.country === 'BR';
      }

      // Caso contrário, verifica se a categoria está presente no array
      return source.categories && source.categories.some(c => c.toLowerCase() === catLower);
    })
    .sort((a, b) => (a.rank || 999) - (b.rank || 999));
}

/**
 * Varre o catálogo unificado e extrai dinamicamente todas as categorias únicas 
 * para gerar as rotas estáticas do Astro.
 */
export function getAllNiches(): string[] {
  const niches = new Set<string>();
  
  catalog.forEach(source => {
    if (source.categories && Array.isArray(source.categories)) {
      source.categories.forEach(cat => niches.add(cat));
    }
  });
  
  return Array.from(niches);
}