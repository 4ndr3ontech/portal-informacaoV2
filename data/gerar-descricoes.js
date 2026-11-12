import fs from 'fs';
import path from 'path';

const INPUT_PATH = path.resolve('data/news-sources.json');
const OUTPUT_PATH = path.resolve('src/data/clean-news-sources.json');

const VALID_CATEGORIES = new Set([
  'brasil', 'mundo', 'politica', 'economia', 'tecnologia', 'games', 'esportes', 'ciencia', 'saude'
]);

const badWords = ['porn', 'sex', 'tube', 'xvideos', 'horny', 'adult', 'escort', 'cam', 'girls', 'nude', 'xxx', 'hentai', 'porno'];

function isSafe(site) {
  const urlLower = site.url.toLowerCase();
  const nameLower = site.name.toLowerCase();
  return !badWords.some(word => urlLower.includes(word) || nameLower.includes(word));
}

function mapCategories(originalCat = '', textContext = '') {
  const catLower = originalCat.toLowerCase();
  const textLower = textContext.toLowerCase();
  const categories = new Set();

  if (/\.br(\/|$)/.test(textLower) || textLower.includes('brasil')) categories.add('brasil');
  if (catLower.includes('tech') || catLower.includes('web') || catLower.includes('tools')) categories.add('tecnologia');
  if (catLower.includes('commerce') || catLower.includes('business')) categories.add('economia');
  if (catLower.includes('sport')) categories.add('esportes');
  if (catLower.includes('game')) categories.add('games');
  if (catLower.includes('science') || catLower.includes('education') || catLower.includes('discovery')) categories.add('ciencia');
  if (catLower.includes('health') || catLower.includes('medical')) categories.add('saude');
  if (catLower.includes('news') || catLower.includes('portals') || catLower.includes('articles')) {
    if (!categories.has('brasil')) categories.add('mundo');
  }

  if (categories.size === 0) {
    if (/economia|finance|business/i.test(textLower)) categories.add('economia');
    else categories.add('mundo');
  }
  return Array.from(categories).filter(c => VALID_CATEGORIES.has(c));
}

function cleanDescription(text) {
  if (!text || text.length < 5) return '';
  let cleanText = text.trim();
  if (!/[.!?]$/.test(cleanText)) {
    const lastSpace = cleanText.lastIndexOf(' ');
    if (lastSpace > 0) {
      cleanText = cleanText.substring(0, lastSpace) + '...';
    } else {
      cleanText += '...';
    }
  }
  return cleanText;
}

console.log('🔄 Processando descrições originais e aplicando filtros...');

if (!fs.existsSync(INPUT_PATH)) {
  console.error(`❌ Erro: O arquivo ${INPUT_PATH} não existe. Execute o script Python primeiro.`);
  process.exit(1);
}

const rawData = JSON.parse(fs.readFileSync(INPUT_PATH, 'utf-8'));
const finalSources = [];

for (const item of rawData) {
  if (!isSafe(item)) continue;

  let domain = '';
  try {
    domain = new URL(item.url).hostname.toLowerCase().replace(/^www\./, '');
  } catch { continue; }

  const nameTrimmed = (item.name || domain).trim();
  const originalDesc = cleanDescription(item.description);

  const finalDescription = originalDesc.length > 10 
    ? `Acesso ao diretório oficial do ${nameTrimmed}. Resumo da plataforma: ${originalDesc}`
    : `Informações e acesso direto ao portal oficial do ${nameTrimmed}.`;

  const combinedContext = `${nameTrimmed} ${item.url} ${originalDesc}`;
  let categories = mapCategories(item.category || '', combinedContext);
  if (categories.length === 0) categories.push('mundo');

  finalSources.push({
    id: domain.replace(/[^a-z0-9]/g, '-'),
    name: nameTrimmed,
    url: item.url.trim(),
    country: categories.includes('brasil') ? 'BR' : 'Global',
    categories: categories,
    description: finalDescription,
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
console.log(`✅ SUCESSO! ${finalSources.length} sites processados em ${OUTPUT_PATH}.`);