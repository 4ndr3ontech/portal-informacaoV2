import type { APIRoute } from 'astro';

export const prerender = false;

// Cabeçalhos JSON obrigatórios para o frontend reconhecer a resposta
const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
};

function json(data: Record<string, unknown>, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: JSON_HEADERS,
  });
}

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const body = await request.json();
    const url = body?.url;

    if (!url) {
      return json({ error: 'URL não fornecido' }, 400);
    }

    let titulo = 'Oferta Especial Mercado Livre';
    let imagem = '/og-default.jpg';
    let preco = '0,00';
    let precoOriginal = '';
    let descricao = 'Produto em destaque selecionado para você.';

    try {
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
          'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        },
        redirect: 'follow'
      });
      
      if (response.ok) {
        const html = await response.text();
        
        // 1. Título e Imagem
        const titleMatch = html.match(/<meta\s+property="og:title"\s+content="([^"]+)"/i) || html.match(/<title>([^<]+)<\/title>/i);
        if (titleMatch) titulo = titleMatch[1].replace(' - Mercado Livre', '').trim();

        const imageMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/i);
        if (imageMatch) imagem = imageMatch[1];

        // 2. Descrição limpa
        const descMatch = html.match(/<meta\s+property="og:description"\s+content="([^"]+)"/i) || html.match(/<meta\s+name="description"\s+content="([^"]+)"/i);
        if (descMatch && descMatch[1]) {
          descricao = descMatch[1]
            .replace(/Compre-o no Mercado Livre/gi, '')
            .replace(/Encontre mais produtos\.?/gi, '')
            .replace(/Olha o que eu encontrei!/gi, '')
            .replace(/Frete grátis em dia\.?/gi, '')
            .trim();
        }

        // 3. CAPTURA PRECISA DE PREÇOS (Original e Promocional)
        // Procura primeiro pelo preço riscado dentro de tags <s> ou blocos de preço original
        const sMatches = [...html.matchAll(/<s[^>]*>([\s\S]*?)<\/s>/gi)];
        for (const sMatch of sMatches) {
          const sContent = sMatch[1];
          const frac = sContent.match(/andes-money-amount__fraction[^>]*>([^<]+)<\/span>/i);
          const cent = sContent.match(/andes-money-amount__cents[^>]*>([^<]+)<\/span>/i);
          if (frac) {
            const intPart = frac[1].replace(/\./g, '').trim();
            const centsPart = cent ? cent[1].trim() : '00';
            precoOriginal = `${intPart},${centsPart}`;
            break;
          }
        }

        // Removemos o bloco riscado do HTML para capturar o preço atual/promocional limpo
        const htmlSemRiscado = html.replace(/<s[^>]*>[\s\S]*?<\/s>/gi, '');
        const fractionMatches = [...htmlSemRiscado.matchAll(/andes-money-amount__fraction[^>]*>([^<]+)<\/span>/gi)];
        const centsMatches = [...htmlSemRiscado.matchAll(/andes-money-amount__cents[^>]*>([^<]+)<\/span>/gi)];

        if (fractionMatches.length > 0) {
          const intPart = fractionMatches[0][1].replace(/\./g, '').trim();
          const centsPart = centsMatches.length > 0 ? centsMatches[0][1].trim() : '00';
          preco = `${intPart},${centsPart}`;
        }

        // Se o preço original for idêntico ao promocional, limpamos o original
        if (preco === precoOriginal) {
          precoOriginal = '';
        }
      }
    } catch (fetchErr) {
      console.warn('⚠️ Aviso no fetch externo:', fetchErr);
    }

    const runtime = (locals as any).runtime;
    const db = runtime?.env?.DB;

    // Se o banco D1 não estiver vinculado localmente, retorna simulação com sucesso
    if (!db) {
      return json({ 
        success: true, 
        message: 'Simulação concluída!',
        data: { titulo, preco, precoOriginal, imagem, descricao, url } 
      });
    }

    // Gravação real no D1
    await db.prepare(
      `INSERT INTO offers (title, description, image_url, affiliate_link, price, original_price, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      titulo, 
      descricao, 
      imagem, 
      url, 
      preco, 
      precoOriginal || null, 
      new Date().toISOString()
    ).run();

    return json({ 
      success: true, 
      data: { titulo, preco, precoOriginal, imagem, descricao } 
    });

  } catch (error: any) {
    return json({ error: error.message || 'Erro no servidor' }, 500);
  }
};