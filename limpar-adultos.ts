import fs from 'fs/promises';

async function removerSitesAdultos() {
  const caminhoFicheiro = './src/data/clean-news-sources.json';
  
  console.log('Lendo a base de dados global...');
  const dados = JSON.parse(await fs.readFile(caminhoFicheiro, 'utf-8'));

  // Lista de palavras-chave e nomes de domínios explícitos (com limites de palavra \b para evitar falsos positivos)
  const regexAdulto = /\b(porn|porno|pornhub|xvideos|redtube|xhamster|brazzers|beeg|milf|xxx|hentai|erotic|erotico|adult|fuq|joymii|freeones|tblop|heaven666)\b/i;

  const sitesLimpos = dados.filter((site: any) => {
    const textoBusca = `${site.name} ${site.url} ${site.description}`.toLowerCase();
    
    // Retorna true APENAS se NÃO encontrar nenhuma palavra-chave adulta
    return !regexAdulto.test(textoBusca);
  });

  const removidos = dados.length - sitesLimpos.length;

  // Grava o arquivo limpo por cima do antigo
  await fs.writeFile(caminhoFicheiro, JSON.stringify(sitesLimpos, null, 2));
  
  console.log(`\n🧹 Limpeza concluída!`);
  console.log(`Total original: ${dados.length} sites`);
  console.log(`Total após limpeza: ${sitesLimpos.length} sites`);
  console.log(`🚨 Foram removidos ${removidos} sites com conteúdo adulto.`);
}

removerSitesAdultos();