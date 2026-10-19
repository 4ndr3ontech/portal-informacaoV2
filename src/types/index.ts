export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
}

export interface NewsSource {
  id: string;
  name: string;
  url: string;
  description: string;
  country: string;
  language: string;
  categories: string[];
  type: 'portal' | 'jornal' | 'revista' | 'agencia' | 'tv' | 'radio';
  active: boolean;
  lastVerified: string;
  isInternational: boolean;
}

export interface AffiliateProduct {
  id: string;
  name: string;
  category: string;
  description: string;
  price?: number;
  lastPriceCheck?: string;
  imageUrl: string;
  originalUrl: string;
  affiliateUrl: string;
  active: boolean;
}