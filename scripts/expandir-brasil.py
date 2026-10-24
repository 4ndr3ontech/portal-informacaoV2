import json
import os
import urllib.request
import urllib.error

# Caminhos dos arquivos
JSON_PATH = os.path.join(os.path.dirname(__file__), '../src/data/brazil-sources.json')

def carregar_fontes():
    if not os.path.exists(JSON_PATH):
        return []
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_fontes(fontes):
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(fontes, f, ensure_ascii=False, indent=2)
    print(f"✅ Arquivo atualizado com sucesso! Total de fontes: {len(fontes)}")

def testar_url(url):
    """Testa se a URL responde (status 200 ou redirecionamento)"""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status < 400
    except Exception:
        return False

def adicionar_novas_fontes():
    fontes_atuais = carregar_fontes()
    urls_existentes = {f.get('url') for f in fontes_atuais}

    # Novas fontes brasileiras para adicionar (Atenção: Use True / False em Python)
    novas_fontes = [
        {
            "name": "The Intercept Brasil",
            "url": "https://www.intercept.com.br",
            "description": "Jornalismo investigativo independente no Brasil.",
            "country": "br",
            "categories": ["geral", "politica"]
        },
        {
            "name": "Agência Pública",
            "url": "https://apublica.org",
            "description": "Primeira agência de jornalismo investigativo sem fins lucrativos do Brasil.",
            "country": "br",
            "categories": ["geral", "investigativo"]
        },
        {
            "name": "Tecnoblog",
            "url": "https://tecnoblog.net",
            "description": "Notícias, análises e tecnologia descomplicada.",
            "country": "br",
            "categories": ["tecnologia"]
        }
    ]

    adicionadas = 0
    for nova in novas_fontes:
        url = nova.get('url')
        if url in urls_existentes:
            print(f"⚠️ Já existe na base: {nova['name']}")
            continue
        
        print(f"🔍 Testando conectividade de: {nova['name']} ({url})...")
        if testar_url(url):
            fontes_atuais.append(nova)
            urls_existentes.add(url)
            adicionadas += 1
            print(f"✔ Adicionado com sucesso!")
        else:
            print(f"❌ URL falhou no teste ou está inacessível: {url}")

    if adicionadas > 0:
        salvar_fontes(fontes_atuais)
    else:
        print("Nenhuma fonte nova foi adicionada.")

if __name__ == "__main__":
    print("🚀 Iniciando expansão e validação de fontes do Brasil...")
    adicionar_novas_fontes()