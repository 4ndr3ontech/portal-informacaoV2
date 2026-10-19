import { describe, it, expect } from 'vitest';
import { products } from '../../src/data/products';
import { sanitizeUrl, getAffiliateLinkProps } from '../../src/lib/links';

describe('Catálogo de Produtos e Links Afiliados', () => {
  it('deve conter produtos válidos e ativos', () => {
    const activeProducts = products.filter((p) => p.active);
    expect(activeProducts.length).toBeGreaterThan(0);
  });

  it('deve possuir atalhos e URLs de destino higienizadas', () => {
    products.forEach((product) => {
      const cleanUrl = sanitizeUrl(product.affiliateUrl);
      expect(cleanUrl).not.toBe('#');
      expect(cleanUrl).toMatch(/^https?:\/\//);
    });
  });

  it('deve fornecer os atributos de rel corretos para links de afiliados', () => {
    const props = getAffiliateLinkProps();
    expect(props.target).toBe('_blank');
    expect(props.rel).toContain('sponsored');
    expect(props.rel).toContain('nofollow');
    expect(props.rel).toContain('noopener');
  });
});