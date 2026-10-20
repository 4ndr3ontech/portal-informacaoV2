import { describe, it, expect } from 'vitest';
import { searchSources } from '../../src/lib/search';
import type { NewsSource } from '../../src/types';

const mockSources: NewsSource[] = [
  {
    id: 'g1',
    name: 'G1',
    url: 'https://g1.globo.com/',
    description: 'Portal de notícias da Globo.',
    country: 'BR',
    language: 'pt-BR',
    categories: ['brasil', 'politica'],
    type: 'portal',
    active: true,
    lastVerified: '2026-10-19',
    isInternational: false
  },
  {
    id: 'bbc',
    name: 'BBC News',
    url: 'https://bbc.com',
    description: 'Notícias internacionais da Grã-Bretanha.',
    country: 'GB',
    language: 'en',
    categories: ['mundo', 'politica'],
    type: 'agencia',
    active: true,
    lastVerified: '2026-10-19',
    isInternational: true
  },
  {
    id: 'inativo',
    name: 'Fonte Inativa',
    url: 'https://inativo.com',
    description: 'Veículo inativo.',
    country: 'BR',
    language: 'pt-BR',
    categories: ['brasil'],
    type: 'portal',
    active: false,
    lastVerified: '2026-10-19',
    isInternational: false
  }
];

describe('searchSources', () => {
  it('deve filtrar fontes ativas e ignorar inativas', () => {
    const results = searchSources(mockSources);
    expect(results).toHaveLength(2);
    expect(results.some((s) => s.id === 'inativo')).toBe(false);
  });

  it('deve buscar por termo no nome e descrição', () => {
    const resultsName = searchSources(mockSources, { query: 'G1' });
    expect(resultsName).toHaveLength(1);
    expect(resultsName[0].id).toBe('g1');

    const resultsDesc = searchSources(mockSources, { query: 'internacionais' });
    expect(resultsDesc).toHaveLength(1);
    expect(resultsDesc[0].id).toBe('bbc');
  });

  it('deve filtrar por categoria', () => {
    const results = searchSources(mockSources, { category: 'mundo' });
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe('bbc');
  });

  it('deve retornar lista vazia se nenhum termo for encontrado', () => {
    const results = searchSources(mockSources, { query: 'termoinexistente123' });
    expect(results).toHaveLength(0);
  });
});