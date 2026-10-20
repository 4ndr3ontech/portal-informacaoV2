import type { Category } from '../types';

export const categories: Category[] = [
  { id: 'brasil', name: 'Brasil', slug: 'brasil', description: 'Principais veículos de notícias com cobertura do território nacional.' },
  { id: 'mundo', name: 'Mundo', slug: 'mundo', description: 'Veículos e agências com cobertura de política e acontecimentos internacionais.' },
  { id: 'politica', name: 'Política', slug: 'politica', description: 'Análises, bastidores e cobertura dos poderes executivo, legislativo e judiciário.' },
  { id: 'economia', name: 'Economia', slug: 'economia', description: 'Mercado financeiro, negócios, indicadores econômicos e finanças pessoais.' },
  { id: 'tecnologia', name: 'Tecnologia', slug: 'tecnologia', description: 'Inovação, inteligência artificial, software, telecomunicações e cultura digital.' },
  { id: 'ciencia', name: 'Ciência', slug: 'ciencia', description: 'Descobertas científicas, astronomia, saúde pública e pesquisas acadêmicas.' },
  { id: 'saude', name: 'Saúde', slug: 'saude', description: 'Bem-estar, medicina, políticas públicas de saúde e avanços médicos.' },
  { id: 'esportes', name: 'Esportes', slug: 'esportes', description: 'Cobertura de futebol, modalidades olímpicas e ligas esportivas globais.' },
  { id: 'educacao', name: 'Educação', slug: 'educacao', description: 'Ensino superior, exames nacionais, pedagogia e políticas educacionais.' },
  { id: 'cultura', name: 'Cultura e Entretenimento', slug: 'cultura', description: 'Cinema, literatura, música, artes visuais e cultura popular.' },
  { id: 'negocios', name: 'Negócios', slug: 'negocios', description: 'Empreendedorismo, startups, gestão e ambiente corporativo.' },
  { id: 'meio-ambiente', name: 'Meio Ambiente', slug: 'meio-ambiente', description: 'Sustentabilidade, mudanças climáticas, biodiversidade e transição energética.' },
];