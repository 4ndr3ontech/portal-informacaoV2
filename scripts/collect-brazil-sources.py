import os
import json
import re
from datetime import datetime
import uuid
import requests
from bs4 import BeautifulSoup

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
SRC_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'src', 'data')

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
            
            # Tenta pegar a descrição do OpenGraph (usada nas redes sociais)
            og_desc = soup.find('meta', property='og:description')
            if og_desc and og_desc.get('content'):
                desc = og_desc['content'].strip()
                if desc: return desc
                
            # Se não encontrar, tenta a meta description padrão de SEO
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc['content'].strip()
                if desc: return desc

    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível capturar de {site_name}. Usando fallback. (Erro: {type(e).__name__})")

    # Retorna a descrição padrão definida no array caso dê erro ou o site bloqueie
    return fallback_desc

BRAZILIAN_RAW_SOURCES = [
    {"name": "G1", "url": "https://g1.globo.com", "categories": ["brasil", "politica", "economia"], "desc": "Principal portal de notícias e jornalismo do Brasil."},
    {"name": "UOL", "url": "https://www.uol.com.br", "categories": ["brasil", "economia", "mundo"], "desc": "Portal pioneiro de notícias, serviços e entretenimento no Brasil."},
    {"name": "Folha de S.Paulo", "url": "https://www.folha.uol.com.br", "categories": ["brasil", "politica", "economia"], "desc": "Um dos principais jornais de referência e circulação nacional."},
    {"name": "Estadão", "url": "https://www.estadao.com.br", "categories": ["brasil", "politica", "economia"], "desc": "Cobertura jornalística abrangente sobre política, economia e cotidiano."},
    {"name": "CNN Brasil", "url": "https://www.cnnbrasil.com.br", "categories": ["brasil", "politica", "economia"], "desc": "Canal de notícias 24 horas e portal de jornalismo político e econômico."},
    {"name": "Metrópoles", "url": "https://www.metropoles.com", "categories": ["brasil", "politica"], "desc": "Portal de notícias com foco em Brasília e grande relevância nacional."},
    {"name": "Terra", "url": "https://www.terra.com.br", "categories": ["brasil", "esportes", "mundo"], "desc": "Portal de notícias, esportes, entretenimento e tecnologia."},
    {"name": "R7", "url": "https://www.r7.com", "categories": ["brasil", "esportes"], "desc": "Portal de notícias e conteúdos multimídia."},
    {"name": "Band", "url": "https://www.band.uol.com.br", "categories": ["brasil", "esportes"], "desc": "Portal de notícias e transmissão do Grupo Bandeirantes."},
    {"name": "SBT News", "url": "https://www.sbtnews.com.br", "categories": ["brasil", "politica"], "desc": "Portal jornalístico do Sistema Brasileiro de Televisão."},
    {"name": "poder360", "url": "https://www.poder360.com.br", "categories": ["brasil", "politica", "economia"], "desc": "Jornalismo digital especializado em política, poder e economia."},
    {"name": "CartaCapital", "url": "https://www.cartacapital.com.br", "categories": ["brasil", "politica"], "desc": "Revista semanal de análise política, econômica e cultural."},
    {"name": "Revista Oeste", "url": "https://revistaoeste.com", "categories": ["brasil", "politica"], "desc": "Jornalismo de opinião, política e economia."},
    {"name": "Brasil 247", "url": "https://www.brasil247.com", "categories": ["brasil", "politica"], "desc": "Portal progressista de notícias e debate político."},
    {"name": "Gazeta do Povo", "url": "https://www.gazetadopovo.com.br", "categories": ["brasil", "politica"], "desc": "Veículo tradicional do Paraná com atuação nacional e foco em opinião."},
    {"name": "Jovem Pan News", "url": "https://jovempan.com.br", "categories": ["brasil", "politica", "esportes"], "desc": "Notícias, rádio e programação jornalística e esportiva."},
    {"name": "Agência Brasil", "url": "https://agenciabrasil.ebc.com.br", "categories": ["brasil", "politica"], "desc": "Empresa Brasil de Comunicação — notícias oficiais e gerais."},
    {"name": "The Intercept Brasil", "url": "https://www.intercept.com.br", "categories": ["brasil", "politica"], "desc": "Jornalismo investigativo independente."},
    {"name": "UOL Notícias", "url": "https://noticias.uol.com.br", "categories": ["brasil", "politica"], "desc": "Editoria de notícias e colunistas do UOL."},
    {"name": "Yahoo Notícias Brasil", "url": "https://br.noticias.yahoo.com", "categories": ["brasil", "mundo"], "desc": "Agregador e portal de notícias."},

    # Tecnologia
    {"name": "Tecnoblog", "url": "https://tecnoblog.net", "categories": ["tecnologia"], "desc": "Independência e tecnologia em primeira mão."},
    {"name": "Canaltech", "url": "https://canaltech.com.br", "categories": ["tecnologia", "ciencia"], "desc": "Análises de produtos, tecnologia e inovação."},
    {"name": "Olhar Digital", "url": "https://olhardigital.com.br", "categories": ["tecnologia", "ciencia"], "desc": "O portal de tecnologia do Brasil."},
    {"name": "TecMundo", "url": "https://www.tecmundo.com.br", "categories": ["tecnologia"], "desc": "Notícias e análises de tecnologia, internet e cultura pop."},
    {"name": "MacMagazine", "url": "https://macmagazine.com.br", "categories": ["tecnologia"], "desc": "O maior site sobre o ecossistema Apple em língua portuguesa."},
    {"name": "TudoCelular", "url": "https://www.tudocelular.com", "categories": ["tecnologia"], "desc": "Especificações, preços e análises de smartphones."},
    {"name": "Adrenaline", "url": "https://www.adrenaline.com.br", "categories": ["tecnologia"], "desc": "Hardware, PC gaming, placas de vídeo e tecnologia."},
    {"name": "Baboo", "url": "https://www.baboo.com.br", "categories": ["tecnologia"], "desc": "Segurança digital, Windows e dicas técnicas."},
    {"name": "Showmetech", "url": "https://www.showmetech.com.br", "categories": ["tecnologia"], "desc": "Reviews de eletrônicos e novidades tecnológicas."},

    # Economia
    {"name": "InfoMoney", "url": "https://www.infomoney.com.br", "categories": ["economia"], "desc": "Mercado financeiro, ações, fundos e economia."},
    {"name": "Valor Econômico", "url": "https://valor.globo.com", "categories": ["economia"], "desc": "O principal jornal de economia e negócios do Brasil."},
    {"name": "Exame", "url": "https://exame.com", "categories": ["economia"], "desc": "Negócios, economia, investimentos e sustentabilidade."},
    {"name": "Forbes Brasil", "url": "https://forbes.com.br", "categories": ["economia"], "desc": "Negócios, inovação, estilo de vida e mercado financeiro."},
    {"name": "Seu Dinheiro", "url": "https://www.seudinheiro.com", "categories": ["economia"], "desc": "Educação financeira, bolsa de valores e criptomoedas."},
    {"name": "Suno Notícias", "url": "https://www.suno.com.br/noticias", "categories": ["economia"], "desc": "Notícias sobre fundos imobiliários, ações e economia."},
    {"name": "Money Times", "url": "https://www.moneytimes.com.br", "categories": ["economia"], "desc": "Mercados financeiros, dólar, cripto e investimentos."},
    {"name": "Pipeline Valor", "url": "https://pipelinevalor.globo.com", "categories": ["economia"], "desc": "M&A, venture capital e mercado corporativo."},
    {"name": "B3 Notícias", "url": "https://www.b3.com.br", "categories": ["economia"], "desc": "Informações oficiais da Bolsa do Brasil."},

    # Esportes / Games
    {"name": "The Enemy", "url": "https://www.theenemy.com.br", "categories": ["esportes"], "desc": "Portal de jogos, e-sports e cultura pop."},
    {"name": "Voxel", "url": "https://www.voxel.com.br", "categories": ["tecnologia"], "desc": "Análises de games, lançamentos e consoles."},
    {"name": "MyPSt", "url": "https://mypst.com.br", "categories": ["esportes"], "desc": "A maior comunidade PlayStation do Brasil."},
    {"name": "Flow Games", "url": "https://flowgames.gg", "categories": ["tecnologia"], "desc": "Portal de games, notícias e análises."},
    {"name": "The Clutch", "url": "https://theclutch.com.br", "categories": ["esportes"], "desc": "Cobertura dedicada a e-sports e cenário competitivo."},
    {"name": "Dust2 Brasil", "url": "https://dust2.com.br", "categories": ["esportes"], "desc": "O principal portal de Counter-Strike do Brasil."},

    # Esportes
    {"name": "ge (Globo Esporte)", "url": "https://ge.globo.com", "categories": ["esportes"], "desc": "Tudo sobre futebol, clubes, tabela do Brasileirão e esportes olímpicos."},
    {"name": "UOL Esporte", "url": "https://www.uol.com.br/esporte", "categories": ["esportes"], "desc": "Notícias, colunistas e cobertura ao vivo de competições esportivas."},
    {"name": "Lance!", "url": "https://www.lance.com.br", "categories": ["esportes"], "desc": "O diário esportivo do torcedor brasileiro."},
    {"name": "ESPN Brasil", "url": "https://www.espn.com.br", "categories": ["esportes"], "desc": "Futebol internacional, NFL, NBA e cobertura global de esportes."},
    {"name": "Gazeta Esportiva", "url": "https://www.gazetaesportiva.com", "categories": ["esportes"], "desc": "Tradição no jornalismo esportivo brasileiro."},
    {"name": "Superesportes", "url": "https://www.mg.superesportes.com.br", "categories": ["esportes"], "desc": "Futebol mineiro e nacional."},

    # Ciência e Saúde
    {"name": "Agência FAPESP", "url": "https://agencia.fapesp.br", "categories": ["ciencia"], "desc": "Divulgação científica e fomento à pesquisa no Brasil."},
    {"name": "Superinteressante", "url": "https://super.abril.com.br", "categories": ["ciencia", "mundo"], "desc": "Ciência, história, comportamento e tecnologia explicados."},
    {"name": "Revista Galileu", "url": "https://revistagalileu.globo.com", "categories": ["ciencia"], "desc": "Ciência, inovação, meio ambiente e exploração espacial."},
    {"name": "CNN Brasil Saúde", "url": "https://www.cnnbrasil.com.br/saude", "categories": ["saude"], "desc": "Avanços médicos, bem-estar e saúde pública."},
    {"name": "Dráuzio Varella", "url": "https://drauziovarella.uol.com.br", "categories": ["saude"], "desc": "Informação confiável sobre saúde, prevenção e medicina."},
    {"name": "Conass", "url": "https://www.conass.org.br", "categories": ["saude"], "desc": "Conselho Nacional de Secretários de Saúde."}
]

def generate_brazil_dataset():
    records = []
    total_sources = len(BRAZILIAN_RAW_SOURCES)
    
    print(f"Iniciando coleta e extração de metadados para {total_sources} fontes...")
    
    for idx, item in enumerate(BRAZILIAN_RAW_SOURCES, start=1):
        clean_name = re.sub(r'[^a-z0-9]', '-', item['name'].lower()).strip('-')
        unique_id = f"br-{clean_name}-{idx}-{str(uuid.uuid5(uuid.NAMESPACE_URL, item['url']))[:6]}"
        
        valid_cats = map_to_valid_categories(item['categories'])
        
        # Chama a função para buscar a descrição real do site (com scraping)
        real_description = fetch_real_description(item['url'], item['name'], item['desc'])
        
        records.append({
            "id": unique_id,
            "rank": idx,
            "name": item['name'],
            "country": "BR",
            "url": item['url'],
            "score": 95.0 - (idx * 0.05),
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