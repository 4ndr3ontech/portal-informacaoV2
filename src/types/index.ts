export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  icon?: string;
}

export interface NewsSource {
  id: string;
  rank?: number | null;
  name: string;
  url: string;
  description?: string;
  country?: string | null;
  language?: string;
  categories: string[];
  type?: 'portal' | 'jornal' | 'revista' | 'agencia' | 'tv' | 'radio' | string;
  score?: number | null;
  source?: string;
  active?: boolean;
  lastVerified?: string;
  isInternational?: boolean;
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