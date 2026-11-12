// Importa a sua base completa e a base enriquecida do Brasil
import fontesOriginais from './clean-news-sources.json';
import fontesBrasilEnriquecidas from './fontes-brasil.json';
import type { NewsSource } from '../types';

// 1. Junta as duas listas colocando os sites do Brasil PRIMEIRO.
// Como o Brasil vem primeiro, a versão com as descrições ricas vence na deduplicação!
const todasFontes = [
  ...(fontesBrasilEnriquecidas as NewsSource[]),
  ...(fontesOriginais as NewsSource[])
];

// 2. Deduplicação automática por ID e ordenação por rank
const seenIds = new Set<string>();
export const sources: NewsSource[] = todasFontes
  .filter(source => {
    if (!source || !source.id) return false;
    const cleanId = source.id.toLowerCase().trim();
    if (seenIds.has(cleanId)) return false; // Se já viu o ID (ex: versão do Brasil), ignora a antiga
    seenIds.add(cleanId);
    return true;
  })
  .sort((a, b) => (a.rank || 999) - (b.rank || 999));

// Funções utilitárias
export function getSourcesByCategory(category: string): NewsSource[] {
  return sources.filter(
    source => source.active && source.categories && source.categories.includes(category)
  );
}

export function getSourcesStatistics() {
  return {
    total: sources.length,
    active: sources.filter(s => s.active).length,
    categoriesCount: new Set(sources.flatMap(s => s.categories)).size
  };
}

export default sources;