import fs from 'fs';
import path from 'path';

const GLOBAL_INPUT_PATH = path.resolve('data/news-sources.json');
const BRAZIL_INPUT_PATH = path.resolve('data/brazil-sources.json');
const OUTPUT_PATH = path.resolve('src/data/clean-news-sources.json');

/**
 * Função para categorizar automaticamente com base no nome e descrição
 */
function categorizeSource(name = '', description = '') {
  const text = `${name} ${description}`.toLowerCase();
  const categories = [];

  if (/tech|tecnologia|software|ia|artificial|hardware|gadget|code|dev|cyber/i.test(text)) categories.push('tecnologia');
  if (/economia|finance|mercado|banco|investimento|money|stocks|crypto|fii/i.test(text)) categories.push('economia');
  if (/politica|governo|congress|senado|deputado|ministerio/i.test(text)) categories.push('politica');
  if (/game|esport|futebol|soccer|basket|playstation|xbox|nintendo/i.test(text)) categories.push('games');
  if (/ciencia|science|space|nasa|astronomy|pesquisa/i.test(text)) categories.push('ciencia');
  if (/saude|health|medicina|hospital|bem-estar|doctor/i.test(text)) categories.push('saude');
  if (/entretenimento|filme|cinema|musica|serie|culture|tv/i.test(text)) categories.push('entretenimento');
  if (/educacao|escola|university|college|student|enem|vestibular/i.test(text)) categories.push('educacao');

  return categories;
}

function processAndMergeSources() {
  console.log('📂 A ler e sincronizar os ficheiros de dados...');

  const seenDomains = new Set();
  const finalSources = [];

  function addSourcesFromFile(filePath, isBrazil = false) {
    if (!fs.existsSync(filePath)) {
      console.warn(`⚠️ Aviso: Ficheiro não encontrado em ${filePath}`);
      return;
    }

    const rawData = fs.readFileSync(filePath, 'utf-8');
    const rawArray = JSON.parse(rawData);
    console.log(`🔍 Processando ${filePath} (${rawArray.length} registos)...`);

    for (const item of rawArray) {
      if (!item || !item.name || !item.url) continue;

      const nameTrimmed = item.name.trim();

      if (!isBrazil) {
        if (nameTrimmed.length <= 2) continue;
        if (nameTrimmed.toLowerCase() === 'sim' && item.description?.toLowerCase().includes('best alternative')) continue;
      }

      let domain = '';
      try {
        const urlObj = new URL(item.url.startsWith('http') ? item.url : `https://${item.url}`);
        domain = urlObj.hostname.toLowerCase().replace(/^www\./, '');
      } catch {
        continue;
      }

      if (seenDomains.has(domain)) continue;
      seenDomains.add(domain);

      // Trata as categorias: garante 'brasil' para fontes nacionais e aplica o mapeamento inteligente
      let categories = Array.isArray(item.categories) ? [...item.categories] : [];
      
      if (isBrazil && !categories.includes('brasil')) {
        categories.push('brasil');
      }

      // Descobre novas categorias com base no conteúdo (nome e descrição)
      const autoCategories = categorizeSource(nameTrimmed, item.description);
      for (const cat of autoCategories) {
        if (!categories.includes(cat)) {
          categories.push(cat);
        }
      }

      // Se ainda estiver sem categoria, define 'geral' ou 'mundo'
      if (categories.length === 0) {
        categories.push(isBrazil ? 'brasil' : 'mundo');
      }

      finalSources.push({
        id: item.id || domain.replace(/[^a-z0-9]/g, '-'),
        name: nameTrimmed,
        url: item.url,
        country: isBrazil ? 'BR' : (item.country || 'Global'),
        categories: categories,
        description: item.description ? item.description.trim() : 'Sem descrição disponível.',
        rss_url: item.rss_url || '',
        favicon: item.favicon || '',
        active: true,
        lastVerified: new Date().toISOString().split('T')[0]
      });
    }
  }

  // Processa o acervo global e depois o do Brasil integrando perfeitamente
  addSourcesFromFile(GLOBAL_INPUT_PATH, false);
  addSourcesFromFile(BRAZIL_INPUT_PATH, true);

  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(finalSources, null, 2), 'utf-8');
  console.log(`✅ Sucesso! Total de ${finalSources.length} fontes únicas unificadas, limpas e sincronizadas guardadas em ${OUTPUT_PATH}`);
}

processAndMergeSources();