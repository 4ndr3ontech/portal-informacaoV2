export interface SEOProps {
  title: string;
  description: string;
  canonicalUrl?: string;
  type?: 'website' | 'article';
  image?: string;
}

export function generateSEOMetadata(props: SEOProps, siteUrl: string = 'https://seusite.com.br') {
  const fullTitle = `${props.title} | PortalInfo`;
  const canonical = props.canonicalUrl || siteUrl;
  const ogImage = props.image || `${siteUrl}/images/og-default.png`;

  return {
    title: fullTitle,
    description: props.description,
    canonical,
    openGraph: {
      title: fullTitle,
      description: props.description,
      url: canonical,
      type: props.type || 'website',
      image: ogImage,
      siteName: 'PortalInfo'
    },
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description: props.description,
      image: ogImage
    }
  };
}