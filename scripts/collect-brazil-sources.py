import os
import json
import re
from datetime import datetime
import uuid
import requests
from bs4 import BeautifulSoup

# Diretórios de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SRC_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'data')
SOURCES_FILE = os.path.join(os.path.dirname(__file__), 'sources.json')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SRC_DATA_DIR, exist_ok=True)

VALID_CATEGORIES = {"brasil", "mundo", "politica", "economia", "tecnologia", "ciencia", "saude", "esportes"}

def map_to_valid_categories(raw_cats):
    mapped = []
    for c in raw_cats:
        c_lower = c.lower().strip()
        if c_lower in VALID_CATEGORIES:
            mapped.append(c_lower)
        elif c_lower in ['hardware', 'software', 'smartphones', 'apple', 'inovacao', 'computadores']:
            mapped.append('tecnologia')
        elif c_lower in ['investimentos', 'negocios', 'financas', 'mercados', 'bolsa', 'bilionarios']:
            mapped.append('economia')
        elif c_lower in ['games', 'esports', 'cultura-pop', 'entretenimento', 'playstation', 'csgo', 'podcast']:
            mapped.append('esportes' if 'esport' in c_lower else 'mundo')
        elif c_lower in ['educacao', 'cultura', 'pesquisa']:
            mapped.append('ciencia')
        elif c_lower in ['medicina', 'bem-estar', 'politica-publica']:
            mapped.append('saude')
        else:
            mapped.append('brasil')
    
    if not mapped:
        mapped = ['brasil']
    return list(set(mapped) & VALID_CATEGORIES) or ['brasil']

def fetch_real_description(url, site_name, fallback_desc):
    """
    Acessa a URL e tenta extrair a descrição oficial (OpenGraph ou Meta Description).
    Retorna o fallback_desc original em caso de falha ou bloqueio do site.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        print(f"Buscando metadados de: {site_name} ({url})...")
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tenta pegar a descrição do OpenGraph
            og_desc = soup.find('meta', property='og:description')
            if og_desc and og_desc.get('content'):
                desc = og_desc['content'].strip()
                if desc: return desc
                
            # Tenta a meta description padrão de SEO
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc['content'].strip()
                if desc: return desc

    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível capturar de {site_name}. Usando fallback. (Erro: {type(e).__name__})")

    return fallback_desc

def generate_brazil_dataset():
    records = []
    
    # Valida a existência do ficheiro sources.json
    if not os.path.exists(SOURCES_FILE):
        print(f"Erro: O arquivo '{SOURCES_FILE}' não foi encontrado.")
        print("Certifique-se de que o sources.json está na mesma pasta que este script.")
        return

    # Carrega os dados
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        sources_data = json.load(f)
        
    # Adapta automaticamente se o JSON for um Dicionário ou uma Lista
    flat_sources = []
    if isinstance(sources_data, dict):
        for sites in sources_data.values():
            flat_sources.extend(sites)
    elif isinstance(sources_data, list):
        flat_sources = sources_data
    else:
        print("Erro: O ficheiro sources.json está num formato não reconhecido.")
        return

    total_sources = len(flat_sources)
    print(f"Iniciando coleta e extração de metadados para {total_sources} fontes...")
    
    for idx, item in enumerate(flat_sources, start=1):
        clean_name = re.sub(r'[^a-z0-9]', '-', item['name'].lower()).strip('-')
        unique_id = f"br-{clean_name}-{idx}-{str(uuid.uuid5(uuid.NAMESPACE_URL, item['url']))[:6]}"
        
        # Lê 'category' (singular) ou 'categories' (plural)
        raw_cats = [item['category']] if 'category' in item else item.get('categories', [])
        valid_cats = map_to_valid_categories(raw_cats)
        
        desc_padrao = item.get('desc', f"Acompanhe as últimas notícias e informações no portal {item['name']}.")
        real_description = fetch_real_description(item['url'], item['name'], desc_padrao)
        
        records.append({
            "id": unique_id,
            "rank": idx,
            "name": item['name'],
            "country": "BR",
            "url": item['url'],
            "score": 95.0 - (idx * 0.01),
            "source": "Curadoria Especializada Brasil",
            "active": True,
            "categories": valid_cats,
            "description": real_description,
            "language": "pt-BR",
            "type": "portal",
            "lastVerified": datetime.now().strftime('%Y-%m-%d'),
            "isInternational": False
        })

    json_path = os.path.join(DATA_DIR, 'brazil-sources.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Sucesso: {len(records)} fontes brasileiras geradas com metadados reais em {json_path}")

if __name__ == "__main__":
    generate_brazil_dataset()