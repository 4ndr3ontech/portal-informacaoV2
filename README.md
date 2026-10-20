# PortalInfo — Portal de Notícias e Ofertas Afiliadas

Diretório independente de fontes de notícias verificadas e seleção editorial de ofertas comerciais do Mercado Livre.

## Tecnologias Principais
- **Framework:** Astro v4 (TypeScript)
- **Hospedagem:** Cloudflare Pages (Estático)
- **Automação CI/CD:** GitHub Actions + Cloudflare Git Integration
- **Suíte de Testes:** Vitest

## Parâmetros de Deploy na Cloudflare Pages
Ao conectar o repositório ao Cloudflare Pages, utilize exatamente os seguintes parâmetros:
- **Framework Preset:** `Astro`
- **Build command:** `npm run build`
- **Build output directory:** `dist`
- **Node.js Version (Variável de Ambiente):** `NODE_VERSION` = `20`

## Comandos do Projeto
- `npm run dev`: Inicia o servidor local de desenvolvimento (`http://localhost:4321`).
- `npm run test`: Executa a suíte de testes unitários e de integridade de dados.
- `npm run build`: Executa a verificação estática de tipos e gera a versão de produção na pasta `dist/`.# portal-informacaoV2
