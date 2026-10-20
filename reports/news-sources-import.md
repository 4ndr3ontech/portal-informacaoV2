# Relatório de Importação — Top 1000 News & Media Platforms

- **Data da execução:** 20/10/2026
- **Fonte original:** `https://top1000.com/top-1000-news-and-media-platforms/`
- **Total de registros coletados:** 1000
- **IDs únicos:** 1000
- **URLs únicas e sanitizadas:** 1000
- **Status da Validação:** ✅ APROVADO SEM ERROS

## Estrutura de Arquivos Gerados
1. `data/news-sources.json` — Cópia estruturada bruta em JSON.
2. `src/data/sources.ts` — Dataset tipado integrado ao Astro.
3. `scripts/import-news-sources.py` — Script automatizado de coleta.
4. `scripts/validate-news-sources.py` — Script de validação de integridade.
5. `reports/news-sources-import.md` — Relatório de execução.

## Procedimento para Reexecução
```bash
source .venv/bin/activate
python3 scripts/import-news-sources.py
python3 scripts/validate-news-sources.py