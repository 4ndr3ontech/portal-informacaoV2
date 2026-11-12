import fs from 'fs/promises';
import { sources } from './src/data/sources'; // Lê diretamente do seu ficheiro TS!

async function extrairDescricaoReal(url: string) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 6000);

    const resposta = await fetch(url, {
      headers: { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' 
      },
      signal: controller.signal
    });
    clearTimeout(timeout);

    if (!resposta.ok) return null;

    const html = await resposta.text();

    const regexDescricao = /<meta[^>]+(?:name|property)=["'](?:og:)?description["'][^>]+content=["']([^"']+)["']/i;
    const regexAlternativa = /<meta[^>]+content=["']([^"']+)["'][^>]+(?:name|property)=["'](?:og:)?description["']/i;

    const match = html.match(regexDescricao) || html.match(regexAlternativa);
    
    return match ? match[1].replace(/(\r\n|\n|\r)/gm, " ").trim() : null;
  } catch (erro) {
    return null;
  }
}

async function iniciarProcesso() {
  console.log(`A ler o sources.ts... Encontrados ${sources.length} sites do Brasil!`);
  
  let atualizados = 0;
  const sitesEnriquecidos = [];

  for (let i = 0; i < sources.length; i++) {
    const site = sources[i];
    console.log(`[${i+1}/${sources.length}] A extrair: ${site.name} (${site.url})...`);
    
    const descricaoReal = await extrairDescricaoReal(site.url);
    
    if (descricaoReal && descricaoReal.length > 10) {
      site.description = descricaoReal;
      // Guardamos também na fullDescription para a sua página de SEO!
      (site as any).fullDescription = descricaoReal; 
      atualizados++;
      console.log(`   ✅ Encontrada: ${descricaoReal.substring(0, 80)}...`);
    } else {
      console.log(`   ❌ Nenhuma descrição válida encontrada.`);
    }
    
    sitesEnriquecidos.push(site);
    
    // Pequena pausa para os servidores não nos bloquearem
    await new Promise(r => setTimeout(r, 1000));
  }

  // Guarda tudo num novo ficheiro JSON dedicado ao Brasil
  await fs.writeFile('./src/data/fontes-brasil.json', JSON.stringify(sitesEnriquecidos, null, 2));
  
  console.log(`\n🎉 Processo concluído! ${atualizados} sites atualizados com as descrições reais.`);
  console.log('👉 Foi gerado o ficheiro: src/data/fontes-brasil.json');
}

iniciarProcesso();