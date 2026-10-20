import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SRC_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'data')

def normalize_url(url):
    if not url:
        return ""
    u = url.lower().strip()
    u = u.replace('https://', '').replace('http://', '').replace('www.', '')
    if u.endswith('/'):
        u = u[:-1]
    # Remove query params de rastreamento para comparação segura
    if '?' in u:
        u = u.split('?')[0]
    return u

def merge_catalogs():
    global_json_path = os.path.join(DATA_DIR, 'news-sources.json')
    br_json_path = os.path.join(DATA_DIR, 'brazil-sources.json')

    global_sources = []
    if os.path.exists(global_json_path):
        with open(global_json_path, 'r', encoding='utf-8') as f:
            global_sources = json.load(f)

    br_sources = []
    if os.path.exists(br_json_path):
        with open(br_json_path, 'r', encoding='utf-8') as f:
            br_sources = json.load(f)

    existing_urls = {normalize_url(s['url']) for s in global_sources}
    
    new_br_added = 0
    skipped_duplicates = 0

    combined = list(global_sources)

    for source in br_sources:
        norm = normalize_url(source['url'])
        if norm in existing_urls:
            skipped_duplicates += 1
            print(f"Duplicidade detectada e ignorada: {source['name']} ({source['url']})")
        else:
            existing_urls.add(norm)
            combined.append(source)
            new_br_added += 1

    # Salva o arquivo final unificado em TypeScript para o Astro
    ts_path = os.path.join(SRC_DATA_DIR, 'sources.ts')
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write("import type { NewsSource } from '../types';\n\n")
        f.write(f"// Catálogo Integrado: {len(global_sources)} Internacionais + {new_br_added} Brasileiros\n\n")
        f.write("export const sources: NewsSource[] = ")
        f.write(json.dumps(combined, ensure_ascii=False, indent=2))
        f.write(";\n")

    print(f"\n--- RELATÓRIO DE INTEGRAÇÃO DO CATÁLOGO ---")
    print(f"Total de Fontes Globais Originais: {len(global_sources)}")
    print(f"Fontes Brasileiras Novas Adicionadas: {new_br_added}")
    print(f"Duplicidades Evitadas: {skipped_duplicates}")
    print(f"Total Geral de Fontes no Repositório: {len(combined)}")

if __name__ == "__main__":
    merge_catalogs()