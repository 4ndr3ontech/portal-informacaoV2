import type { NewsSource } from '../types';

export interface SearchOptions {
  query?: string;
  category?: string;
  country?: string;
  language?: string;
}

export function searchSources(sources: NewsSource[], options: SearchOptions = {}): NewsSource[] {
  return sources.filter((source) => {
    // Ignora fontes inativas
    if (source.active === false) {
      return false;
    }

    // Filtro de Categoria
    if (options.category) {
      const targetCat = options.category.toLowerCase().trim();
      const hasCat = source.categories?.some((c) => c.toLowerCase() === targetCat);
      if (!hasCat) return false;
    }

    // Filtro de País
    if (options.country) {
      if (!source.country || source.country.toLowerCase() !== options.country.toLowerCase()) {
        return false;
      }
    }

    // Filtro de Idioma
    if (options.language) {
      if (!source.language || source.language.toLowerCase() !== options.language.toLowerCase()) {
        return false;
      }
    }

    // Busca Textual Geral
    if (options.query) {
      const q = options.query.toLowerCase().trim();
      const nameMatch = source.name.toLowerCase().includes(q);
      const descMatch = (source.description || '').toLowerCase().includes(q);
      const countryMatch = (source.country || '').toLowerCase().includes(q);
      const catMatch = source.categories?.some((c) => c.toLowerCase().includes(q));

      if (!nameMatch && !descMatch && !countryMatch && !catMatch) {
        return false;
      }
    }

    return true;
  });
}