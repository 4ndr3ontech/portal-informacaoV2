import type { APIRoute } from 'astro';

export const prerender = false;

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const body = await request.json();
    const url = body?.url;

    if (!url) {
      return new Response(JSON.stringify({ error: 'URL não fornecido' }), { status: 400 });
    }

    let titulo = 'Oferta Especial Mercado Livre';
    let imagem = '/og-default.jpg';
    let preco = '0,00';
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
        
        // Extração de Título
        const titleMatch = html.match(/<meta\s+property="og:title"\s+content="([^"]+)"/i) ||
                           html.match(/<title>([^<]+)<\/title>/i);
        if (titleMatch) titulo = titleMatch[1].replace(' - Mercado Livre', '').trim();

        // Extração de Imagem
        const imageMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/i);
        if (imageMatch) imagem = imageMatch[1];

        // Extração de Preço (Múltiplas tentativas para o formato do Mercado Livre)
        const priceFractionMatch = html.match(/<span\s+class="andes-money-amount__fraction"[^>]*>([^<]+)<\/span>/i);
        const priceMetaMatch = html.match(/<meta\s+itemprop="price"\s+content="([^"]+)"/i);
        const jsonLdPriceMatch = html.match(/"price"\s*:\s*"([0-9.]+)"/i);

        if (priceFractionMatch) {
          preco = priceFractionMatch[1].trim();
        } else if (priceMetaMatch) {
          // Formata o preço vindo da meta tag para o padrão brasileiro (ex: 1529,10 ou 1.200)
          const rawPrice = priceMetaMatch[1];
          preco = Number(rawPrice).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        } else if (jsonLdPriceMatch) {
          const rawPrice = jsonLdPriceMatch[1];
          preco = Number(rawPrice).toLocaleString('pt-BR', { minimumFractionDigits: 2 });
        }
      }
    } catch (fetchErr) {
      console.warn('⚠️ Aviso no fetch externo:', fetchErr);
    }

    const runtime = (locals as any).runtime;
    const db = runtime?.env?.DB;

    if (!db) {
      return new Response(JSON.stringify({ 
        success: true, 
        message: 'Simulação concluída com sucesso!',
        data: { titulo, preco, imagem, url } 
      }), { status: 200 });
    }

    // Gravação real no Cloudflare D1
    await db.prepare(
      `INSERT INTO offers (title, description, image_url, affiliate_link, price, created_at) VALUES (?, ?, ?, ?, ?, ?)`
    ).bind(
      titulo, 
      descricao, 
      imagem, 
      url, 
      preco, 
      new Date().toISOString()
    ).run();

    return new Response(JSON.stringify({ 
      success: true, 
      data: { titulo, preco, imagem } 
    }), { status: 200 });

  } catch (error: any) {
    console.error('❌ Erro crítico:', error);
    return new Response(JSON.stringify({ error: error.message || 'Erro no servidor' }), { status: 500 });
  }
};