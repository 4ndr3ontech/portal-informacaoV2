import json
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import uuid

# ==============================================================================
# CONFIGURAÇÕES DE CAMINHOS
# ==============================================================================
DATA_DIR = 'data'
SRC_DATA_DIR = 'src/data'
JSON_OUTPUT_PATH = os.path.join(DATA_DIR, 'news-sources.json')
TS_OUTPUT_PATH = os.path.join(SRC_DATA_DIR, 'sources.ts')
FONTE_ORIGINAL = "http://5000best.com/websites/"

# ==============================================================================
# 1. FUNÇÃO DE CATEGORIZAÇÃO INTELIGENTE
# ==============================================================================
def classificar_site(url, descricao):
    """
    Analisa a URL e a descrição extraída para atribuir as categorias corretas
    do portal MundoEmUmCLICK.
    """
    texto = (url + " " + descricao).lower()
    categorias = []
    
    # Mapeamento de palavras-chave para as 12 categorias do portal
    if any(p in texto for p in ['brazil', 'brasil', 'brazilian', '.br']):
        categorias.append('brasil')
    if any(p in texto for p in ['world', 'international', 'global', 'news', 'journal', 'daily']):
        categorias.append('mundo')
    if any(p in texto for p in ['politic', 'government', 'election', 'policy', 'congress', 'democrat', 'republican']):
        categorias.append('politica')
    if any(p in texto for p in ['economy', 'business', 'market', 'trade', 'commerce', 'corporate']):
        categorias.append('economia')
    if any(p in texto for p in ['tech', 'technology', 'software', 'hardware', 'digital', 'computer', 'cyber', 'app']):
        categorias.append('tecnologia')
    if any(p in texto for p in ['science', 'space', 'astronomy', 'physics', 'biology', 'research', 'discovery']):
        categorias.append('ciencia')
    if any(p in texto for p in ['health', 'medical', 'fitness', 'wellness', 'medicine', 'doctor', 'clinic', 'hospital']):
        categorias.append('saude')
    if any(p in texto for p in ['sport', 'football', 'soccer', 'basketball', 'tennis', 'nfl', 'nba', 'athletics']):
        categorias.append('esportes')
    if any(p in texto for p in ['game', 'gaming', 'esports', 'playstation', 'xbox', 'nintendo', 'casino', 'poker']):
        categorias.append('games')
    if any(p in texto for p in ['entertainment', 'movie', 'music', 'film', 'celebrity', 'tv', 'show', 'hollywood', 'art', 'culture', 'gossip']):
        categorias.append('entretenimento')
    if any(p in texto for p in ['education', 'school', 'university', 'college', 'student', 'learn', 'academy', 'course']):
        categorias.append('educacao')
    if any(p in texto for p in ['investment', 'finance', 'stock', 'crypto', 'bitcoin', 'fund', 'forex', 'trading', 'wealth', 'investing']):
        categorias.append('investimentos')
        
    # Categoria de fallback (padrão) caso o script não encontre nenhuma correspondência
    if not categorias:
        categorias.append('mundo')
        
    return categorias

# ==============================================================================
# 2. COLETAR A LISTA DO SITE ORIGEM COM PAGINAÇÃO (50 Páginas)
# ==============================================================================
def coletar_fontes_do_site_origem(url_origem, limite_de_paginas=50):
    print(f"A iniciar a recolha em {limite_de_paginas} páginas de: {url_origem}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    fontes_brutas = []
    urls_vistas = set() 
    ignorar_dominios = ['5000best.com', 'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'pinterest.com']
    
    for pagina in range(1, limite_de_paginas + 1):
        url_atual = url_origem if pagina == 1 else f"{url_origem.rstrip('/')}/{pagina}/"
        print(f"\n-> A extrair URLs da Página {pagina}: {url_atual}")
        
        try:
            response = requests.get(url_atual, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Fim das páginas alcançado (Código {response.status_code}).")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            elementos = soup.find_all('a')
            sites_adicionados_nesta_pagina = 0
            
            for item in elementos:
                url_veiculo = item.get('href', '').strip()
                nome_veiculo = item.text.strip()
                
                if not url_veiculo or url_veiculo.startswith(('/', '#', 'mailto:', 'javascript:')):
                    continue
                if any(dominio in url_veiculo for dominio in ignorar_dominios):
                    continue
                if url_veiculo.startswith('www.'):
                    url_veiculo = 'http://' + url_veiculo
                    
                if url_veiculo.startswith('http'):
                    if not nome_veiculo:
                        nome_veiculo = url_veiculo.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
                    
                    if url_veiculo not in urls_vistas:
                        urls_vistas.add(url_veiculo)
                        index = len(fontes_brutas) + 1
                        fontes_brutas.append({
                            "id": f"site-{index}-{str(uuid.uuid4())[:6]}",
                            "name": nome_veiculo.capitalize(),
                            "url": url_veiculo,
                            "country": "INT"
                        })
                        sites_adicionados_nesta_pagina += 1
                        
                        if len(fontes_brutas) >= 5000:
                            break
                            
            print(f"   Encontrados {sites_adicionados_nesta_pagina} sites válidos nesta página.")
            if sites_adicionados_nesta_pagina == 0 or len(fontes_brutas) >= 5000:
                break
            time.sleep(1.5)
            
        except Exception as e:
            print(f"Erro ao aceder à página {pagina}: {e}")
            break
            
    print(f"\nTotal de sites capturados para análise de metadados: {len(fontes_brutas)}")
    return fontes_brutas

# ==============================================================================
# 3. EXTRAIR METADADOS DE CADA SITE
# ==============================================================================
def enriquecer_dados_do_site(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    dados_extras = {"description_rich": "", "rss_url": "", "favicon": ""}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            dados_extras["description_rich"] = meta_desc.get('content').strip()
            
        rss_link = soup.find('link', type='application/rss+xml') or soup.find('link', type='application/atom+xml')
        if rss_link and rss_link.get('href'):
            dados_extras["rss_url"] = urljoin(url, rss_link.get('href'))
            
        icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
        if icon_link and icon_link.get('href'):
            dados_extras["favicon"] = urljoin(url, icon_link.get('href'))
    except Exception:
        pass 
        
    return dados_extras

# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================
def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SRC_DATA_DIR, exist_ok=True)
    
    fontes_brutas = coletar_fontes_do_site_origem(FONTE_ORIGINAL)
    
    if not fontes_brutas:
        print("Nenhum site extraído.")
        return

    fontes_processadas = []
    
    print("\nA iniciar a classificação e extração de metadados (Isto pode demorar algum tempo)...")
    for indice, fonte in enumerate(fontes_brutas, start=1):
        print(f"[{indice}/{len(fontes_brutas)}] A analisar: {fonte['name']}")
        
        extras = enriquecer_dados_do_site(fonte['url'])
        descricao = extras["description_rich"] if extras["description_rich"] else "Sem descrição disponível."
        
        # Chama a nova função para descobrir a categoria com base na descrição e URL raspadas
        categorias_identificadas = classificar_site(fonte['url'], descricao)
        
        fonte_enriquecida = {
            **fonte,
            "categories": categorias_identificadas,
            "description": descricao,
            "rss_url": extras["rss_url"],
            "favicon": extras["favicon"],
            "active": True,
            "lastVerified": time.strftime("%Y-%m-%d")
        }
        
        fontes_processadas.append(fonte_enriquecida)
        time.sleep(0.3)

    # Guarda o JSON na pasta data/
    with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(fontes_processadas, f, ensure_ascii=False, indent=2)
    
    # ATENÇÃO: A correção foi feita aqui! Trocamos 'Source' por 'NewsSource'.
    ts_content = "import type { NewsSource } from '../types';\n\nexport const sources: NewsSource[] = "
    ts_content += json.dumps(fontes_processadas, ensure_ascii=False, indent=2)
    ts_content += ";\n"

    with open(TS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(ts_content)
        
    print(f"\n✅ Concluído! {len(fontes_processadas)} sites processados, classificados e guardados.")

if __name__ == "__main__":
    main()