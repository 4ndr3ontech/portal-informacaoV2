import fs from 'fs';
import path from 'path';

const INPUT_PATH = path.resolve('data/news-sources.json');
const OUTPUT_PATH = path.resolve('src/data/clean-news-sources.json');

const VALID_CATEGORIES = new Set([
  'brasil', 'mundo', 'politica', 'economia', 'tecnologia', 'games', 'esportes', 'ciencia', 'saude'
]);

// Termos proibidos: Redes Sociais, Conteúdo Adulto, E-commerce, Buscadores, Softwares, Ferramentas Web e Culinária/Delivery
const blockedKeywords = [
  // Redes sociais e chats
  'facebook', 'instagram', 'twitter', 'x.com', 'pinterest', 'linkedin', 
  'tumblr', 'reddit', 'tiktok', 'snapchat', 'whatsapp', 'telegram', 
  'discord', 'twitch', 'vk.com', 'myspace', 'flickr', 'imgur',
  // Conteúdo adulto / dating
  'chaturbate', 'porno', 'sex', 'tube', 'xvideos', 'horny', 'adult', 
  'escort', 'cam', 'girls', 'nude', 'xxx', 'hentai', 'dating', 'match',
  // Lojas, E-commerce e Varejo
  'shop', 'store', 'shopping', 'buy', 'cart', 'market', 'commerce', 
  'deal', 'coupon', 'price', 'sale', 'auction', 'ebay', 'amazon', 
  'walmart', 'etsy', 'classified', 'classifieds', 'realestate', 'rentals',
  // Buscadores e Motores de Pesquisa
  'search', 'engine', 'lookup', 'crawler', 'finder', 'webcrawler',
  // Software, Antivírus, Utilitários e Downloads de Programas
  'antivirus', 'software', 'download', 'freeware', 'shareware', 'codec',
  'player', 'cleaner', 'driver', 'utility', 'toolkit', 'plugin', 'extension',
  'malware', 'firewall', 'security', 'keygen', 'crack', 'torrent',
  // Ferramentas para Internet, Hospedagem, SEO e Utilitários Web
  'hosting', 'domain', 'dns', 'seo', 'analyzer', 'counter', 'traffic',
  'submit', 'directory', 'webmaster', 'stats', 'analytics', 'validator',
  'generator', 'hosting24', 'vps', 'server', 'ssl', 'ip-',
  // Delivery, Alimentos, Culinária, Receitas e Restaurantes
  'food', 'delivery', 'recipe', 'recipes', 'restaurant', 'restaurants', 
  'pizza', 'cooking', 'kitchen', 'chef', 'menu', 'eat', 'burger', 'snack'
];

function detectCountry(url, categories) {
  const lowerUrl = url.toLowerCase();
  if (lowerUrl.includes('.br') || categories.includes('brasil')) return 'BR';
  if (lowerUrl.includes('.pt')) return 'PT';
  if (lowerUrl.includes('.ar')) return 'AR';
  if (lowerUrl.includes('.uk') || lowerUrl.includes('.co.uk')) return 'GB';
  if (lowerUrl.includes('.us') || lowerUrl.includes('.gov')) return 'US';
  if (lowerUrl.includes('.fr')) return 'FR';
  if (lowerUrl.includes('.de')) return 'DE';
  if (lowerUrl.includes('.es')) return 'ES';
  if (lowerUrl.includes('.it')) return 'IT';
  return 'Global';
}

function isNewsOrValidPortal(site) {
  const urlLower = site.url.toLowerCase();
  const nameLower = site.name.toLowerCase();
  const descLower = (site.description || '').toLowerCase();

  if (urlLower.includes('google.com') && !urlLower.includes('news.google')) {
    return false;
  }

  const isExcluded = blockedKeywords.some(keyword => 
    urlLower.includes(keyword) || 
    nameLower.includes(keyword) || 
    descLower.includes(` ${keyword} `) ||
    descLower.includes(`${keyword}.`)
  );

  return !isExcluded;
}

function mapCategories(originalCat = '', textContext = '') {
  const catLower = originalCat.toLowerCase();
  const textLower = textContext.toLowerCase();
  const categories = new Set();

  // Mapeamento específico para Política
  if (
    catLower.includes('politi') || 
    catLower.includes('gov') || 
    catLower.includes('law') || 
    catLower.includes('civic') ||
    textLower.includes('politics') || 
    textLower.includes('policy') || 
    textLower.includes('government') || 
    textLower.includes('election') || 
    textLower.includes('congress') ||
    textLower.includes('governo') ||
    textLower.includes('eleições')
  ) {
    categories.add('politica');
  }

  if (/\.br(\/|$)/.test(textLower) || textLower.includes('brasil')) categories.add('brasil');
  if (catLower.includes('tech') || catLower.includes('web') || catLower.includes('tools')) categories.add('tecnologia');
  if (catLower.includes('commerce') || catLower.includes('business') || catLower.includes('finance')) categories.add('economia');
  if (catLower.includes('sport')) categories.add('esportes');
  if (catLower.includes('game')) categories.add('games');
  if (catLower.includes('science') || catLower.includes('education') || catLower.includes('discovery')) categories.add('ciencia');
  if (catLower.includes('health') || catLower.includes('medical')) categories.add('saude');
  
  if (catLower.includes('news') || catLower.includes('portals') || catLower.includes('articles')) {
    if (!categories.has('brasil') && !categories.has('politica')) categories.add('mundo');
  }

  if (categories.size === 0) {
    if (/economia|finance|business/i.test(textLower)) categories.add('economia');
    else categories.add('mundo');
  }
  return Array.from(categories).filter(c => VALID_CATEGORIES.has(c));
}

console.log('🔄 Processando portais, aplicando regras de Política e deteção de países...');

if (!fs.existsSync(INPUT_PATH)) {
  console.error(`❌ Erro: Arquivo ${INPUT_PATH} não encontrado.`);
  process.exit(1);
}

const rawData = JSON.parse(fs.readFileSync(INPUT_PATH, 'utf-8'));
const finalSources = [];
const removedSites = [];

for (const item of rawData) {
  if (!isNewsOrValidPortal(item)) {
    removedSites.push({ name: item.name, url: item.url, reason: 'Filtro de bloqueio' });
    continue;
  }

  let domain = '';
  try {
    domain = new URL(item.url).hostname.toLowerCase().replace(/^www\./, '');
  } catch { continue; }

  const nameTrimmed = (item.name || domain).trim();
  const rawDesc = item.description ? item.description.trim() : '';

  const isGenericOrEmpty = !rawDesc || rawDesc === '&nbsp;' || rawDesc.length < 5 || rawDesc.toLowerCase().includes('portal oficial');

  if (isGenericOrEmpty) {
    removedSites.push({ name: nameTrimmed, url: item.url, reason: 'Sem descrição real' });
    continue;
  }

  const combinedContext = `${nameTrimmed} ${item.url} ${rawDesc} ${item.category || ''}`;
  let categories = mapCategories(item.category || '', combinedContext);
  if (categories.size === 0) categories.add('mundo');

  const countryCode = detectCountry(item.url, categories);

  finalSources.push({
    id: domain.replace(/[^a-z0-9]/g, '-'),
    name: nameTrimmed,
    url: item.url.trim(),
    country: countryCode,
    categories: categories,
    description: rawDesc,
    rank: item.rank,
    score: item.score,
    audience: item.audience,
    favicon: `https://www.google.com/s2/favicons?domain=${domain}&sz=128`,
    active: true,
    lastVerified: new Date().toISOString().split('T')[0]
  });
}

const outputDir = path.dirname(OUTPUT_PATH);
if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

fs.writeFileSync(OUTPUT_PATH, JSON.stringify(finalSources, null, 2), 'utf-8');
console.log(`\n✅ SUCESSO! Base atualizada com ${finalSources.length} portais e países detetados.`);