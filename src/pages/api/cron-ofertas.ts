const novasOfertas = [
      {
        title: 'Oferta em Destaque 1 - E-commerce / Admitad',
        description: 'Primeiro produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 89,90',
        original_price: 'R$ 129,90'
      },
      {
        title: 'Oferta em Destaque 2 - E-commerce / Admitad',
        description: 'Segundo produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 149,90',
        original_price: 'R$ 199,90'
      },
      {
        title: 'Oferta em Destaque 3 - E-commerce / Admitad',
        description: 'Terceiro produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 59,90',
        original_price: 'R$ 89,90'
      },
      {
        title: 'Oferta em Destaque 4 - E-commerce / Admitad',
        description: 'Quarto produto selecionado automaticamente no lote.',
        image_url: '/og-default.jpg',
        affiliate_link: 'https://omundoemumclick.com.br',
        price: 'R$ 199,90',
        original_price: 'R$ 259,90'
      }
    ];

    for (const oferta of novasOfertas) {
      await db.prepare(
        `INSERT INTO offers (title, description, image_url, affiliate_link, price, original_price, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)`
      ).bind(
        oferta.title, 
        oferta.description, 
        oferta.image_url, 
        oferta.affiliate_link, 
        oferta.price,
        oferta.original_price,
        new Date().toISOString()
      ).run();
    }