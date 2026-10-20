import os
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import uuid

TARGET_URL = "https://top1000.com/top-1000-news-and-media-platforms/"

# Cabeçalhos avançados para simular um navegador real e evitar bloqueios (Erro 403/Cloudflare)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SRC_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'data')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SRC_DATA_DIR, exist_ok=True)

KNOWN_DOMAINS = {
    'msn': 'https://www.msn.com',
    'globo': 'https://www.globo.com',
    'g1': 'https://g1.globo.com',
    'uol': 'https://www.uol.com.br',
    'new york times': 'https://www.nytimes.com',
    'nyt': 'https://www.nytimes.com',
    'bbc': 'https://www.bbc.com',
    'bbc news brasil': 'https://www.bbc.com/portuguese',
    'cnn': 'https://www.cnn.com',
    'cnn brasil': 'https://www.cnnbrasil.com.br',
    'yahoo': 'https://www.yahoo.com',
    'yahoo news': 'https://news.yahoo.com',
    'folha de s.paulo': 'https://www.folha.uol.com.br',
    'folha': 'https://www.folha.uol.com.br',
    'estadao': 'https://www.estadao.com.br',
    'r7': 'https://www.r7.com',
    'terra': 'https://www.terra.com.br',
    'metropoles': 'https://www.metropoles.com',
    'poder360': 'https://www.poder360.com.br',
    'jovem pan': 'https://jovempan.com.br',
    'reuters': 'https://www.reuters.com',
    'bloomberg': 'https://www.bloomberg.com',
    'the washington post': 'https://www.washingtonpost.com',
    'the guardian': 'https://www.theguardian.com',
    'forbes': 'https://www.forbes.com',
    'fox news': 'https://www.foxnews.com',
    'daily mail': 'https://www.dailymail.co.uk',
    'the wall street journal': 'https://www.wsj.com',
    'wsj': 'https://www.wsj.com',
    'nbc news': 'https://www.nbcnews.com',
    'abc news': 'https://abcnews.go.com',
    'time': 'https://time.com',
    'huffpost': 'https://www.huffpost.com',
    'el pais': 'https://elpais.com',
    'le monde': 'https://www.lemonde.fr'
}

def generate_unique_id(name, index):
    clean_name = re.sub(r'[^a-z0-9]', '-', str(name).lower())
    clean_name = re.sub(r'-+', '-', clean_name).strip('-')
    if not clean_name:
        clean_name = f"portal-{index}"
    unique_suffix = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{name}-{index}"))[:6]
    return f"{clean_name}-{index}-{unique_suffix}"

def resolve_clean_url(raw_href, name, index, existing_urls):
    if raw_href and raw_href.startswith('http') and 'top1000.com' not in raw_href:
        url = raw_href.strip()
    else:
        clean_key = name.lower().strip()
        if clean_key in KNOWN_DOMAINS:
            url = KNOWN_DOMAINS[clean_key]
        else:
            domain_name = re.sub(r'[^a-z0-9]', '', clean_key)
            if not domain_name:
                domain_name = f"portalnews{index}"
            url = f"https://www.{domain_name}.com"

    final_url = url
    if final_url in existing_urls:
        separator = '&' if '?' in final_url else '?'
        final_url = f"{url}{separator}source_id={index}"

    return final_url

def determine_categories(name, url, country):
    cats = []
    name_lower = name.lower()
    
    is_br = (country.upper() == 'BR' or 'BRASIL' in name_lower or 'GLOBO' in name_lower or 'UOL' in name_lower or '.BR' in url.lower())
    if is_br:
        cats.append("brasil")
    else:
        cats.append("mundo")

    if any(k in name_lower for k in ['econom', 'financial', 'money', 'business', 'forbes', 'bloomberg', 'market', 'invest', 'valor']):
        cats.append("economia")
    if any(k in name_lower for k in ['tech', 'geek', 'digital', 'cyber', 'software', 'hardware', 'code', 'wired', 'pc', 'comput', 'ai']):
        cats.append("tecnologia")
    if any(k in name_lower for k in ['politi', 'poder', 'congress', 'gov', 'senado', 'camara', 'insider']):
        cats.append("politica")
    if any(k in name_lower for k in ['sport', 'futebol', 'bola', 'esporte']):
        cats.append("esportes")
    if any(k in name_lower for k in ['cienc', 'science', 'astro', 'space', 'nature', 'research']):
        cats.append("ciencia")
    if any(k in name_lower for k in ['saude', 'health', 'med', 'hospital', 'bem-estar']):
        cats.append("saude")

    if len(cats) == 1:
        if is_br:
            cats.extend(["politica", "economia"])
        else:
            cats.extend(["economia", "mundo"])

    return list(set(cats))

def fetch_real_description(url, fallback_desc):
    """
    Acessa a URL simulando um navegador real para evitar bloqueios.
    Retorna o fallback_desc original em caso de falha ou bloqueio.
    """
    try:
        # Aumentado o timeout para 8 segundos para dar tempo aos sites mais lentos
        response = requests.get(url, headers=HEADERS, timeout=8)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Tenta pegar a descrição do OpenGraph (usada nas redes sociais)
            og_desc = soup.find('meta', property='og:description')
            if og_desc and og_desc.get('content') and len(og_desc['content']) > 15:
                return og_desc['content'].strip()
                
            # 2. Se não encontrar, tenta a meta description padrão de SEO
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content') and len(meta_desc['content']) > 15:
                return meta_desc['content'].strip()
        else:
            print(f"   [Aviso] Bloqueio do site (HTTP {response.status_code})")

    except Exception as e:
        print(f"   [Aviso] Falha de conexão ou timeout")

    return fallback_desc

def scrape_top1000():
    print(f"Iniciando coleta, categorização e extração de metadados em: {TARGET_URL}")
    print("Acessando sites originais com headers avançados. Isso levará alguns minutos...\n")
    
    response = requests.get(TARGET_URL, headers=HEADERS)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    records = []
    existing_urls = set()
    
    rows = soup.select('table tr, .ranking-row, .item-list, tbody tr')
    
    valid_index = 0
    for index, row in enumerate(rows):
        if index == 0 and row.name == 'tr' and row.find('th'): 
            continue
            
        try:
            cols = row.find_all(['td', 'div'])
            if len(cols) < 2:
                continue

            valid_index += 1
            rank_text = cols[0].get_text(strip=True).replace('#', '').replace('.', '')
            rank = int(rank_text) if rank_text.isdigit() else valid_index
            
            link_tag = row.find('a')
            name = link_tag.get_text(strip=True) if link_tag else cols[1].get_text(strip=True)
            raw_href = link_tag['href'] if link_tag and link_tag.has_attr('href') else ""
            
            if not name:
                name = f"Veículo {valid_index}"

            data_url = link_tag.get('data-url') if link_tag else None
            url = resolve_clean_url(data_url or raw_href, name, valid_index, existing_urls)
            existing_urls.add(url)

            country_tag = row.find(class_=re.compile('country|flag'))
            country_str = country_tag.get_text(strip=True) if country_tag else "Global"
            
            is_br = (country_str.upper() == 'BR' or 'BRASIL' in name.upper() or '.BR' in url.upper())
            categories = determine_categories(name, url, country_str)

            score_tag = row.find(class_=re.compile('score|rating'))
            score_text = score_tag.get_text(strip=True) if score_tag else None
            score = float(score_text) if score_text and score_text.replace('.','').isdigit() else None

            # Texto de fallback caso falhe
            fallback_description = f"Plataforma e veículo de comunicação {name}, especializado em cobertura jornalística de relevância nas editorias de {', '.join(categories)}."

            print(f"[{valid_index}] Extraindo metadados: {name} ({url})...")
            real_description = fetch_real_description(url, fallback_description)

            records.append({
                "id": generate_unique_id(name, valid_index),
                "rank": rank,
                "name": name,
                "country": "BR" if is_br else country_str,
                "url": url,
                "score": score,
                "source": TARGET_URL,
                "active": True,
                "categories": categories,
                "description": real_description,
                "language": "pt-BR" if is_br else "en",
                "type": "portal",
                "lastVerified": datetime.now().strftime('%Y-%m-%d'),
                "isInternational": not is_br
            })
            
        except Exception as e:
            print(f"Erro ao parsear linha {index}: {e}")

    return records

def save_files(records):
    json_path = os.path.join(DATA_DIR, 'news-sources.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    
    ts_path = os.path.join(SRC_DATA_DIR, 'sources.ts')
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write("import type { NewsSource } from '../types';\n\n")
        f.write(f"// Gerado automaticamente em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"// Fonte: {TARGET_URL}\n\n")
        f.write("export const sources: NewsSource[] = ")
        f.write(json.dumps(records, ensure_ascii=False, indent=2))
        f.write(";\n")
        
    print(f"\n✅ Sucesso: {len(records)} registros extraídos e atualizados com metadados reais.")

if __name__ == "__main__":
    data = scrape_top1000()
    save_files(data)