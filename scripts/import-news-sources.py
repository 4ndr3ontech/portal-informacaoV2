import urllib.request
import json
import os
import re
import time

OUTPUT_FILE = 'data/news-sources.json'
BASE_URL = 'http://5000best.com/websites/?p='

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', raw_html)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    return ' '.join(text.split()).strip()

def fetch_sites():
    print("🌍 Iniciando extração avançada de todas as descrições reais do 5000best...")
    sites = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for page in range(1, 51):
        url = f"{BASE_URL}{page}"
        print(f"📄 Processando página {page}/50...")
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            # Divide a página por linhas da tabela
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.IGNORECASE | re.DOTALL)
            
            for row in rows:
                cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.IGNORECASE | re.DOTALL)
                
                if len(cols) >= 5:
                    rank_raw = clean_html(cols[0])
                    score = clean_html(cols[1] if len(cols) > 1 else "")
                    category = clean_html(cols[2] if len(cols) > 2 else "")
                    audience = clean_html(cols[3] if len(cols) > 3 else "")
                    url_col = cols[4] if len(cols) > 4 else ""
                    
                    # Procura a coluna que tem o texto mais longo (que é obrigatoriamente a Descrição)
                    # ou pega a última coluna útil da linha se houver mais de 5 colunas
                    description_raw = ""
                    if len(cols) >= 7:
                        description_raw = clean_html(cols[6])
                    elif len(cols) == 6:
                        description_raw = clean_html(cols[5])
                    
                    # Se ainda estiver vazia, varre todas as colunas para achar a que tem texto descritivo longo
                    if not description_raw or len(description_raw) < 5:
                        for col in cols:
                            text_candidate = clean_html(col)
                            if len(text_candidate) > 25 and not "http" in text_candidate and not text_candidate.isdigit():
                                description_raw = text_candidate
                                break

                    rank_match = re.search(r'\d+', rank_raw)
                    
                    if rank_match:
                        rank = int(rank_match.group())
                        url_match = re.search(r'href=["\'](.*?)["\']', url_col, re.IGNORECASE)
                        full_url = ""
                        domain_name = clean_html(url_col)
                        
                        if url_match:
                            full_url = url_match.group(1).strip()
                            if not full_url.startswith('http'):
                                full_url = 'http://' + full_url
                                
                        if domain_name:
                            sites.append({
                                "rank": rank,
                                "score": score,
                                "category": category,
                                "audience": audience,
                                "name": domain_name.capitalize(),
                                "url": full_url,
                                "description": description_raw if description_raw else f"Portal oficial do site {domain_name}."
                            })
                            
        except Exception as e:
            print(f"❌ Erro na página {page}: {e}")
            
        time.sleep(0.3)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sites, f, indent=2, ensure_ascii=False)

    print(f"✅ SUCESSO! {len(sites)} sites extraídos com suas respetivas descrições.")

if __name__ == '__main__':
    fetch_sites()