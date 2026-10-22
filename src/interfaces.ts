// 1. Vocabulário Controlado de Nichos (Categorias)
export type CategoryId = 
  | 'brasil'
  | 'mundo'
  | 'politica'
  | 'economia'
  | 'tecnologia'
  | 'esportes'
  | 'ciencia'
  | 'saude';

// 2. Tipagem de País e Idioma (Prevenindo anomalias de "Breitbart como BR")
export type CountryCode = 'BR' | 'US' | 'UK' | 'PT' | string; // Expansível conforme a auditoria avança
export type LanguageCode = 'pt-BR' | 'en-US' | 'en-GB' | 'es-ES' | string;

// 3. Modelo de Dados Principal (Ficha do Veículo)
export interface NewsSource {
  id: string;
  rank: number;
  name: string;
  country: CountryCode;
  url: string;
  score: number;
  source: string;
  active: boolean;
  categories: CategoryId[]; // Força o uso exclusivo dos nichos definidos acima
  description: string;
  language: LanguageCode;
  type: string; // Ex: 'portal', 'jornal', 'revista'
  lastVerified: string; // Formato esperado: YYYY-MM-DD
  isInternational: boolean;
}