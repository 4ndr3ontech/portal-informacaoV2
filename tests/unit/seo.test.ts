import { describe, it, expect } from 'vitest';
import { generateSEOMetadata } from '../../src/lib/seo';

describe('Geração de Metadados de SEO', () => {
  it('deve formatar o título da página corretamente com a marca', () => {
    const meta = generateSEOMetadata({
      title: 'Diretório de Notícias',
      description: 'Descrição de teste.'
    });

    expect(meta.title).toBe('Diretório de Notícias | PortalInfo');
    expect(meta.openGraph.title).toBe('Diretório de Notícias | PortalInfo');
  });

  it('deve usar a URL canonical informada ou fallback padrão', () => {
    const metaCustom = generateSEOMetadata({
      title: 'Teste',
      description: 'Desc',
      canonicalUrl: 'https://seusite.com.br/noticias'
    });

    expect(metaCustom.canonical).toBe('https://seusite.com.br/noticias');
  });
});