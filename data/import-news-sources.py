import urllib.request
import json
import os
import re
import time

OUTPUT_FILE = 'data/news-sources.json'
BASE_URL = 'http://5000best.com/websites/?p='

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).strip()

def fetch_sites():
    print("🌍 Iniciando extração completa dos sites do 5000best...")
    sites = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for page in range(1, 51):
        url = f"{BASE_URL}{page}"
        print(f"📄 Extraindo página {page}/50...")
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.IGNORECASE | re.DOTALL)
            
            for row in rows:
                cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.IGNORECASE | re.DOTALL)
                
                if len(cols) >= 7:
                    rank_raw = clean_html(cols[0])
                    score = clean_html(cols[1])
                    category = clean_html(cols[2])
                    audience = clean_html(cols[3])
                    url_col = cols[4]
                    description = clean_html(cols[6])
                    
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
                                "description": description
                            })
                            
        except Exception as e:
            print(f"❌ Erro na página {page}: {e}")
            
        time.sleep(1)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sites, f, indent=2, ensure_ascii=False)

    print(f"✅ Sucesso total! {len(sites)} sites extraídos e salvos em {OUTPUT_FILE}")

if __name__ == '__main__':
    fetch_sites()