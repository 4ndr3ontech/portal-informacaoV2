import type { NewsSource, Category } from '../types';
import brazilSources from '../data/brazil-sources.json';
import { sources as fontesOriginais } from '../data/sources';

// Une e deduplica o catálogo completo de fontes baseado no nome em minúsculas
const rawSources: NewsSource[] = [...fontesOriginais, ...(brazilSources as NewsSource[])];
const seenNames = new Set<string>();

const catalog: NewsSource[] = rawSources.filter(source => {
  if (!source || !source.name) return false;
  const key = source.name.toLowerCase().trim();
  if (seenNames.has(key)) return false;
  seenNames.add(key);
  return true;
});

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
  return catalog
    .filter(source => source.active !== false && source.categories && source.categories.includes(category as any))
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