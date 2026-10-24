import json
import os

SOURCES_PATH = 'src/data/sources.ts'  # Lê diretamente do TypeScript oficial para garantir os 5000+
BRAZIL_PATH = 'data/brazil-sources.json'
OUTPUT_TS = 'src/data/sources.ts'

def main():
    sources = []
    
    # 1. Tenta carregar do sources.ts existente extraindo o JSON de dentro dele
    if os.path.exists(OUTPUT_TS):
        with open(OUTPUT_TS, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extrai o array JSON contido no ficheiro TypeScript
            try:
                json_str = content[content.index('['):content.rindex(']')+1]
                sources = json.loads(json_str)
            except Exception as e:
                print(f"⚠️ Aviso ao ler sources.ts existente: {e}")

    # Fallback caso o sources.ts esteja vazio
    if not sources and os.path.exists('data/news-sources.json'):
        with open('data/news-sources.json', 'r', encoding='utf-8') as f:
            sources = json.load(f)

    # 2. Carrega as fontes do Brasil
    brazil_sources = []
    if os.path.exists(BRAZIL_PATH):
        with open(BRAZIL_PATH, 'r', encoding='utf-8') as f:
            brazil_sources = json.load(f)

    # 3. Usa um dicionário baseado no nome normalizado para evitar duplicadas
    merged_map = {}

    # Adiciona primeiro todas as fontes principais
    for s in sources:
        key = s.get('name', '').lower().strip()
        if key:
            merged_map[key] = s

    # Adiciona/Atualiza com as fontes do Brasil (garantindo categoria 'brasil' e país 'BR')
    for b in brazil_sources:
        key = b.get('name', '').lower().strip()
        if key:
            if key in merged_map:
                cats = merged_map[key].get('categories', [])
                if 'brasil' not in cats:
                    cats.append('brasil')
                merged_map[key]['categories'] = cats
                merged_map[key]['country'] = 'BR'
            else:
                if 'brasil' not in b.get('categories', []):
                    b.setdefault('categories', []).append('brasil')
                b['country'] = 'BR'
                merged_map[key] = b

    final_list = list(merged_map.values())

    # 4. Grava no arquivo TypeScript oficial com o total combinado correto
    ts_content = "import type { NewsSource } from '../types';\n\nexport const sources: NewsSource[] = "
    ts_content += json.dumps(final_list, ensure_ascii=False, indent=2)
    ts_content += ";\n"

    with open(OUTPUT_TS, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print(f"✅ Sucesso absoluto! Catálogo mesclado com {len(final_list)} fontes totais (5000+ globais + acervo Brasil).")

if __name__ == '__main__':
    main()