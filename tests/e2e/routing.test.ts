import { describe, it, expect } from 'vitest';
import { sources } from '../../src/data/sources';
import { categories } from '../../src/data/categories';
import { products } from '../../src/data/products';

describe('Integridade das Rotas, Dados e Links', () => {
  it('todas as fontes ativas devem possuir IDs unicos e categorias validas', () => {
    const ids = new Set<string>();
    const categorySlugs = new Set(categories.map((c) => c.slug));

    sources.forEach((source) => {
      expect(ids.has(source.id)).toBe(false);
      ids.add(source.id);

      expect(source.name.trim().length).toBeGreaterThan(0);
      expect(source.url).toMatch(/^https?:\/\//);

      source.categories.forEach((catSlug) => {
        expect(categorySlugs.has(catSlug)).toBe(true);
      });
    });
  });

  it('todas as categorias cadastradas devem possuir slug e nome definidos', () => {
    categories.forEach((category) => {
      expect(category.slug).toMatch(/^[a-z0-9-]+$/);
      expect(category.name.trim().length).toBeGreaterThan(0);
    });
  });

  it('todos os produtos de afiliados ativos devem possuir preço valido e URL segura', () => {
    const activeProducts = products.filter((p) => p.active);

    activeProducts.forEach((product) => {
      expect(product.affiliateUrl).toMatch(/^https?:\/\//);
      if (product.price !== undefined) {
        expect(product.price).toBeGreaterThan(0);
      }
    });
  });
});