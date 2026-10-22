import type { NewsSource, Category } from '../types';
import brazilSources from '../data/brazil-sources.json';

// Forçamos a tipagem dos dados importados do JSON
const catalog = brazilSources as NewsSource[];

/**
 * Filtra o catálogo por um nicho específico, retornando apenas fontes ativas.
 * Adicionado fallback `|| 999` para evitar erro de null/undefined no rank.
 */
export function getSourcesByCategory(category: string | Category): NewsSource[] {
  return catalog
    .filter(source => source.active && source.categories && source.categories.includes(category as any))
    .sort((a, b) => (a.rank || 999) - (b.rank || 999));
}

/**
 * Varre o JSON inteiro e extrai dinamicamente todas as categorias únicas 
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