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
        
        // Título e Imagem
        const titleMatch = html.match(/<meta\s+property="og:title"\s+content="([^"]+)"/i) || html.match(/<title>([^<]+)<\/title>/i);
        if (titleMatch) titulo = titleMatch[1].replace(' - Mercado Livre', '').trim();

        const imageMatch = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/i);
        if (imageMatch) imagem = imageMatch[1];

        // CAPTURA DE PREÇOS (Desconto e Original)
        // O Mercado Livre costuma ter múltiplos blocos de preço (o riscado e o promocional)
        const fractionMatches = [...html.matchAll(/<span\s+class="andes-money-amount__fraction"[^>]*>([^<]+)<\/span>/gi)];
        const centsMatches = [...html.matchAll(/<span\s+class="andes-money-amount__cents"[^>]*>([^<]+)<\/span>/gi)];

        if (fractionMatches.length >= 2) {
          // Se houver dois ou mais, o primeiro costuma ser o preço original (riscado) e o segundo o promocional
          const origInt = fractionMatches[0][1].trim();
          const origCents = centsMatches.length > 0 ? centsMatches[0][1].trim() : '00';
          precoOriginal = `${origInt},${origCents}`;

          const promoInt = fractionMatches[1][1].trim();
          const promoCents = centsMatches.length > 1 ? centsMatches[1][1].trim() : '00';
          preco = `${promoInt},${promoCents}`;
        } else if (fractionMatches.length === 1) {
          // Apenas um preço disponível
          const intPart = fractionMatches[0][1].trim();
          const centsPart = centsMatches.length > 0 ? centsMatches[0][1].trim() : '00';
          preco = `${intPart},${centsPart}`;
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
        message: 'Simulação concluída!',
        data: { titulo, preco, precoOriginal, imagem, url } 
      }), { status: 200 });
    }

    // Gravação real no D1 (incluindo o preço original)
    await db.prepare(
      `INSERT INTO offers (title, description, image_url, affiliate_link, price, original_price, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      titulo, 
      descricao, 
      imagem, 
      url, 
      preco, 
      precoOriginal, 
      new Date().toISOString()
    ).run();

    return new Response(JSON.stringify({ 
      success: true, 
      data: { titulo, preco, precoOriginal, imagem } 
    }), { status: 200 });

  } catch (error: any) {
    return new Response(JSON.stringify({ error: error.message || 'Erro no servidor' }), { status: 500 });
  }
};