import { describe, it, expect } from 'vitest';
import { products } from '../../src/data/products';

describe('Painel Administrativo e Métricas', () => {
  it('deve conter produtos válidos mapeados para exibição no painel', () => {
    expect(products.length).toBeGreaterThan(0);
    products.forEach((p) => {
      expect(p.id).toBeTypeOf('string');
      expect(p.name).toBeTypeOf('string');
    });
  });

  it('deve garantir que todos os produtos tenham identificadores únicos no dashboard', () => {
    const ids = new Set(products.map((p) => p.id));
    expect(ids.size).toBe(products.length);
  });
});