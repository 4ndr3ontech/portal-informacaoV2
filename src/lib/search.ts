import type { NewsSource } from '../types';

export interface SearchOptions {
  query?: string;
  category?: string;
  country?: string;
  language?: string;
  isInternational?: boolean;
}

export function searchSources(sources: NewsSource[], options: SearchOptions = {}): NewsSource[] {
  return sources.filter((source) => {
    if (!source.active) return false;

    if (options.category && options.category !== 'todas') {
      if (!source.categories.includes(options.category)) {
        return false;
      }
    }

    if (options.country) {
      if (source.country.toLowerCase() !== options.country.toLowerCase()) {
        return false;
      }
    }

    if (options.language) {
      if (source.language.toLowerCase() !== options.language.toLowerCase()) {
        return false;
      }
    }

    if (options.isInternational !== undefined) {
      if (Boolean(source.isInternational) !== options.isInternational) {
        return false;
      }
    }

    if (options.query) {
      const q = options.query.trim().toLowerCase();
      if (!q) return true;

      const nameMatch = source.name.toLowerCase().includes(q);
      const descMatch = source.description.toLowerCase().includes(q);
      const countryMatch = source.country.toLowerCase().includes(q);
      const categoryMatch = source.categories.some((cat) => cat.toLowerCase().includes(q));

      return nameMatch || descMatch || countryMatch || categoryMatch;
    }

    return true;
  });
}