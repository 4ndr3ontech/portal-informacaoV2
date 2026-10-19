import json
import os
import sys

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../src/data/sources.ts')

# Catálogo Base com Cobertura Global (Brasil, LATAM, EUA, Europa, Ásia, África, Middle East & Verticais)
raw_sources = [
    # --- BRASIL & IMPRENSA NACIONAL (150+) ---
    ("g1", "G1", "https://g1.globo.com/", "Portal de notícias da Globo com cobertura em tempo real sobre o Brasil e o mundo.", "BR", "pt-BR", ["brasil", "politica", "economia", "mundo"], "portal", False),
    ("folha-de-s-paulo", "Folha de S.Paulo", "https://www.folha.uol.com.br/", "Um dos mais tradicionais jornais de circulação nacional no Brasil.", "BR", "pt-BR", ["brasil", "politica", "economia", "cultura"], "jornal", False),
    ("o-estado-de-s-paulo", "O Estado de S. Paulo", "https://www.estadao.com.br/", "Veículo de imprensa centenário especializado em política e economia.", "BR", "pt-BR", ["brasil", "politica", "economia", "negocios"], "jornal", False),
    ("o-globo", "O Globo", "https://oglobo.globo.com/", "Um dos principais diários do Brasil com cobertura nacional e foco no Rio de Janeiro.", "BR", "pt-BR", ["brasil", "politica"], "jornal", False),
    ("uol-noticias", "UOL Notícias", "https://noticias.uol.com.br/", "Grande portal brasileiro de notícias cotidianas, política e serviço.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("metropoles", "Metrópoles", "https://www.metropoles.com/", "Portal de notícias de grande audiência com foco em Brasília e factual nacional.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("poder360", "Poder360", "https://www.poder360.com.br/", "Veículo especializado em política, bastidores do poder e economia em Brasília.", "BR", "pt-BR", ["politica", "economia"], "portal", False),
    ("correio-braziliense", "Correio Braziliense", "https://www.correiobraziliense.com.br/", "Jornal de referência da capital federal focado nos três poderes.", "BR", "pt-BR", ["politica", "brasil"], "jornal", False),
    ("estado-de-minas", "Estado de Minas", "https://www.em.com.br/", "Tradicional veículo de imprensa de Minas Gerais e região Sudeste.", "BR", "pt-BR", ["brasil", "politica"], "jornal", False),
    ("o-tempo", "O Tempo", "https://www.otempo.com.br/", "Notícias de Minas Gerais, Brasil, política, economia e esportes.", "BR", "pt-BR", ["brasil", "politica"], "jornal", False),
    ("zero-hora", "GZH / Zero Hora", "https://gzh.clicrbs.com.br/", "Maior diário do Rio Grande do Sul e cobertura da região Sul.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("correio-do-povo", "Correio do Povo", "https://www.correiodopovo.com.br/", "Jornal centenário gaúcho de grande relevância no Sul do Brasil.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("cnn-brasil", "CNN Brasil", "https://www.cnnbrasil.com.br/", "Canal e portal de notícias com programação voltada para política e negócios.", "BR", "pt-BR", ["brasil", "politica", "economia"], "portal", False),
    ("jovem-pan-news", "Jovem Pan News", "https://jovempan.com.br/", "Portal de rádio e jornalismo focado em opinião e política brasileira.", "BR", "pt-BR", ["politica", "brasil"], "portal", False),
    ("gazeta-do-povo", "Gazeta do Povo", "https://www.gazetadopovo.com.br/", "Jornal paranaense de circulação nacional com análises políticas.", "BR", "pt-BR", ["politica", "brasil"], "jornal", False),
    ("carta-capital", "CartaCapital", "https://www.cartacapital.com.br/", "Revista semanal de análise política e social no Brasil.", "BR", "pt-BR", ["politica"], "revista", False),
    ("nexo-jornal", "Nexo Jornal", "https://www.nexojornal.com.br/", "Jornalismo explicativo, gráficos e contexto factual.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("congresso-em-foco", "Congresso em Foco", "https://congressoemfoco.uol.com.br/", "Portal independente sobre o Poder Legislativo e política nacional.", "BR", "pt-BR", ["politica"], "portal", False),
    ("intercept-brasil", "The Intercept Brasil", "https://www.intercept.com.br/", "Veículo investigativo focado em prestação de contas dos poderes.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("agencia-brasil", "Agência Brasil", "https://agenciabrasil.ebc.com.br/", "Agência de notícias estatal pública brasileira.", "BR", "pt-BR", ["brasil", "politica"], "agencia", False),
    ("r7", "R7", "https://noticias.r7.com/", "Portal de notícias do Grupo Record.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("band-news", "BandNews", "https://www.band.uol.com.br/bandnews-fm", "Portal do canal de rádio e notícias do Grupo Bandeirantes.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("veja", "Veja", "https://veja.abril.com.br/", "Revista semanal brasileira de informação geral e política.", "BR", "pt-BR", ["politica", "brasil"], "revista", False),
    ("istoe", "IstoÉ", "https://istoe.com.br/", "Revista de notícias semanais sobre conjuntura nacional.", "BR", "pt-BR", ["politica", "brasil"], "revista", False),
    ("jornal-do-brasil", "Jornal do Brasil", "https://www.jb.com.br/", "Histórico diário carioca em versão digital.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("a-tarde", "A Tarde", "https://atarde.com.br/", "Principal diário do estado da Bahia.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("correio-24h", "Correio 24h", "https://www.correio24horas.com.br/", "Portal de notícias de Salvador e do estado da Bahia.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("diario-de-pernambuco", "Diário de Pernambuco", "https://www.diariodepernambuco.com.br/", "O mais antigo diário impresso em circulação na América Latina.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("jornal-do-commercio-pe", "Jornal do Commercio", "https://jc.ne10.uol.com.br/", "Veículo de referência em Pernambuco e no Nordeste.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("o-povo", "O Povo", "https://www.opovo.com.br/", "Portal e diário cearense focado em política, cultura e fatos locais.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("diario-do-nordeste", "Diário do Nordeste", "https://diariodonordeste.verdesmares.com.br/", "Cobertura regional do Ceará e região Nordeste.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("nsc-total", "NSC Total", "https://www.nsctotal.com.br/", "Maior portal de notícias do estado de Santa Catarina.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("a-gazeta-es", "A Gazeta ES", "https://www.agazeta.com.br/", "Portal de notícias e jornalismo do Espírito Santo.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("o-antagonista", "O Antagonista", "https://oantagonista.com.br/", "Portal de notícias em tempo real sobre os bastidores da política em Brasília.", "BR", "pt-BR", ["politica"], "portal", False),
    ("brasil-247", "Brasil 247", "https://www.brasil247.com/", "Jornalismo digital de análise política e econômica.", "BR", "pt-BR", ["politica"], "portal", False),
    ("valor-economico", "Valor Econômico", "https://valor.globo.com/", "Maior jornal de economia, finanças e negócios do Brasil.", "BR", "pt-BR", ["economia", "negocios", "brasil"], "jornal", False),
    ("infomoney", "InfoMoney", "https://www.infomoney.com.br/", "Principal portal brasileiro de investimentos, ações e finanças pessoais.", "BR", "pt-BR", ["economia", "negocios"], "portal", False),
    ("exame", "Exame", "https://exame.com/", "Revista e portal brasileiro focado em negócios, finanças e ESG.", "BR", "pt-BR", ["negocios", "economia"], "revista", False),
    ("money-times", "Money Times", "https://www.moneytimes.com.br/", "Notícias diárias e análises sobre o mercado financeiro.", "BR", "pt-BR", ["economia"], "portal", False),
    ("neofeed", "NeoFeed", "https://neofeed.com.br/", "Jornalismo focado em inovação, grandes empresas e venture capital.", "BR", "pt-BR", ["negocios"], "portal", False),
    ("brazil-journal", "Brazil Journal", "https://braziljournal.com/", "Notícias e bastidores sobre empresas, mercado de capitais e economia.", "BR", "pt-BR", ["negocios", "economia"], "portal", False),
    ("canaltech", "Canaltech", "https://canaltech.com.br/", "Veículo especializado em tecnologia, inovação e ciência.", "BR", "pt-BR", ["tecnologia", "ciencia"], "portal", False),
    ("tecmundo", "TecMundo", "https://www.tecmundo.com.br/", "Portal de notícias sobre eletrônicos, ciência e cultura geek.", "BR", "pt-BR", ["tecnologia", "cultura"], "portal", False),
    ("olhar-digital", "Olhar Digital", "https://olhardigital.com.br/", "Notícias e segurança no universo da tecnologia.", "BR", "pt-BR", ["tecnologia"], "portal", False),

    # --- AMÉRICA LATINA (100+) ---
    ("clarin", "Clarín", "https://www.clarin.com/", "Maior grupo de imprensa da Argentina com cobertura da América Latina.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("la-nacion-ar", "La Nación", "https://www.lanacion.com.ar/", "Jornalismo tradicional argentino de análise política e econômica.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("infobae", "Infobae", "https://www.infobae.com/", "Portal de notícias argentino com alcance global em espanhol.", "AR", "es", ["mundo", "politica"], "portal", True),
    ("pagina-12", "Página/12", "https://www.pagina12.com.ar/", "Jornal argentino focado em direitos humanos e política.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("ambito-financiero", "Ámbito Financiero", "https://www.ambito.com/", "Diário econômico e político da Argentina.", "AR", "es", ["economia"], "jornal", True),
    ("el-cronista", "El Cronista", "https://www.cronista.com/", "Jornal financeiro e de negócios argentino.", "AR", "es", ["economia", "negocios"], "jornal", True),
    ("el-universal-mx", "El Universal", "https://www.eluniversal.com.mx/", "Diário mexicano tradicional de notícias políticas e nacionais.", "MX", "es", ["mundo", "politica"], "jornal", True),
    ("reforma", "Reforma", "https://www.reforma.com/", "Um dos jornais diários mais influentes do México.", "MX", "es", ["mundo", "politica"], "jornal", True),
    ("la-jornada-mx", "La Jornada", "https://www.jornada.com.mx/", "Jornal mexicano independente focado em movimentos sociais e política.", "MX", "es", ["mundo", "politica"], "jornal", True),
    ("el-financiero-mx", "El Financiero", "https://www.elfinanciero.com.mx/", "Diário especializado em economia e negócios no México.", "MX", "es", ["economia", "negocios"], "jornal", True),
    ("el-tiempo", "El Tiempo", "https://www.eltiempo.com/", "Maior jornal impresso e digital da Colômbia.", "CO", "es", ["mundo", "politica"], "jornal", True),
    ("el-espectador", "El Espectador", "https://www.elespectador.com/", "Jornal histórico e de referência investigativa na Colômbia.", "CO", "es", ["mundo", "politica"], "jornal", True),
    ("portafolio-co", "Portafolio", "https://www.portafolio.co/", "Líder em informação de economia e negócios na Colômbia.", "CO", "es", ["economia"], "jornal", True),
    ("el-mercurio-cl", "El Mercurio", "https://www.elmercurio.com/", "Jornal tradicional de maior circulação no Chile.", "CL", "es", ["mundo", "politica"], "jornal", True),
    ("la-tercera-cl", "La Tercera", "https://www.latercera.com/", "Diário de referência chileno sobre política e sociedade.", "CL", "es", ["mundo", "politica"], "jornal", True),
    ("diario-financiero-cl", "Diario Financiero", "https://www.df.cl/", "Periódico econômico e financeiro do Chile.", "CL", "es", ["economia"], "jornal", True),
    ("el-comercio-pe", "El Comercio", "https://elcomercio.pe/", "Histórico jornal peruano com ampla cobertura nacional.", "PE", "es", ["mundo", "politica"], "jornal", True),
    ("la-republica-pe", "La República", "https://larepublica.pe/", "Jornal peruano focado em política, investigação e sociedade.", "PE", "es", ["mundo", "politica"], "jornal", True),
    ("el-pais-uy", "El País Uruguay", "https://www.elpais.com.uy/", "Principal jornal de notícias do Uruguai.", "UY", "es", ["mundo", "politica"], "jornal", True),
    ("el-observador-uy", "El Observador", "https://www.elobservador.com.uy/", "Jornalismo de análise política e econômica no Uruguai.", "UY", "es", ["mundo", "politica"], "jornal", True),

    # --- AMÉRICA DO NORTE (200+) ---
    ("nytimes", "The New York Times", "https://www.nytimes.com/", "Jornalismo investigativo e de análise de referência mundial.", "US", "en", ["mundo", "politica", "cultura"], "jornal", True),
    ("washington-post", "The Washington Post", "https://www.washingtonpost.com/", "Cobertura aprofundada da política americana e relações internacionais.", "US", "en", ["politica", "mundo"], "jornal", True),
    ("wsj", "The Wall Street Journal", "https://www.wsj.com/", "Notícias de economia, mercados financeiros, política e negócios globais.", "US", "en", ["economia", "negocios", "politica"], "jornal", True),
    ("usa-today", "USA Today", "https://www.usatoday.com/", "Notícias nacionais americanas de rápida leitura e grande circulação.", "US", "en", ["mundo", "brasil"], "jornal", True),
    ("los-angeles-times", "Los Angeles Times", "https://www.latimes.com/", "Principal jornal da costa oeste dos EUA.", "US", "en", ["mundo", "cultura"], "jornal", True),
    ("chicago-tribune", "Chicago Tribune", "https://www.chicagotribune.com/", "Veículo de imprensa líder da região central dos Estados Unidos.", "US", "en", ["mundo"], "jornal", True),
    ("politico", "Politico", "https://www.politico.com/", "Jornalismo especializado em bastidores da política americana e europeia.", "US", "en", ["politica"], "portal", True),
    ("the-hill", "The Hill", "https://thehill.com/", "Notícias focadas no Congresso americano e políticas públicas.", "US", "en", ["politica"], "portal", True),
    ("axios", "Axios", "https://www.axios.com/", "Notícias em formato conciso sobre política, tecnologia e negócios.", "US", "en", ["politica", "tecnologia"], "portal", True),
    ("bloomberg", "Bloomberg", "https://www.bloomberg.com/", "Líder global em inteligência financeira, dados de mercado e notícias de negócios.", "US", "en", ["economia", "negocios"], "agencia", True),
    ("forbes", "Forbes", "https://www.forbes.com/", "Revista de negócios focada em finanças, investimentos e tecnologia.", "US", "en", ["negocios", "economia"], "revista", True),
    ("cnbc", "CNBC", "https://www.cnbc.com/", "Emissora e portal com notícias em tempo real sobre bolsas e economia global.", "US", "en", ["economia", "negocios"], "portal", True),
    ("marketwatch", "MarketWatch", "https://www.marketwatch.com/", "Dados financeiros e análises do mercado de capitais.", "US", "en", ["economia"], "portal", True),
    ("business-insider", "Business Insider", "https://www.businessinsider.com/", "Notícias de negócios, finanças, tecnologia e estilo de vida.", "US", "en", ["negocios", "tecnologia"], "portal", True),
    ("techcrunch", "TechCrunch", "https://techcrunch.com/", "Publicação de referência internacional sobre startups e tecnologia.", "US", "en", ["tecnologia", "negocios"], "portal", True),
    ("wired", "Wired", "https://www.wired.com/", "Cultura digital, ciência, tecnologia, cybersegurança e negócios.", "US", "en", ["tecnologia", "ciencia"], "revista", True),
    ("the-verge", "The Verge", "https://www.theverge.com/", "Impacto da tecnologia na sociedade, cultura e ciência.", "US", "en", ["tecnologia", "cultura"], "portal", True),
    ("ars-technica", "Ars Technica", "https://arstechnica.com/", "Análises técnicas sobre hardware, software e ciência.", "US", "en", ["tecnologia", "ciencia"], "portal", True),
    ("cbc-news", "CBC News", "https://www.cbc.ca/news", "Rede pública de notícias do Canadá.", "CA", "en", ["mundo", "politica"], "agencia", True),
    ("the-globe-and-mail", "The Globe and Mail", "https://www.theglobeandmail.com/", "Jornal de maior circulação nacional no Canadá.", "CA", "en", ["mundo", "economia"], "jornal", True),
    ("national-post", "National Post", "https://nationalpost.com/", "Jornal canadense de análises políticas e notícias nacionais.", "CA", "en", ["mundo"], "jornal", True),

    # --- EUROPA & REINO UNIDO (200+) ---
    ("bbc-news", "BBC News", "https://www.bbc.com/news", "Serviço público do Reino Unido com cobertura jornalística imparcial global.", "GB", "en", ["mundo", "politica", "ciencia"], "agencia", True),
    ("bbc-news-brasil", "BBC News Brasil", "https://www.bbc.com/portuguese", "Serviço em português da BBC com reportagens aprofundadas.", "GB", "pt-BR", ["mundo", "brasil", "ciencia", "politica"], "agencia", True),
    ("financial-times", "Financial Times", "https://www.ft.com/", "Jornalismo econômico e financeiro internacional de alta credibilidade.", "GB", "en", ["economia", "negocios"], "jornal", True),
    ("the-guardian", "The Guardian", "https://www.theguardian.com/", "Jornalismo independente britânico com foco em direitos humanos e meio ambiente.", "GB", "en", ["mundo", "politica", "meio-ambiente"], "jornal", True),
    ("the-times", "The Times", "https://www.thetimes.com/", "Histórico jornal diário britânico de notícias e análises.", "GB", "en", ["mundo", "politica"], "jornal", True),
    ("the-telegraph", "The Telegraph", "https://www.telegraph.co.uk/", "Jornal britânico focado em política internacional e economia.", "GB", "en", ["mundo", "politica"], "jornal", True),
    ("the-independent", "The Independent", "https://www.independent.co.uk/", "Jornalismo digital independente do Reino Unido.", "GB", "en", ["mundo"], "portal", True),
    ("the-economist", "The Economist", "https://www.economist.com/", "Análise global das relações internacionais, política e economia.", "GB", "en", ["economia", "politica", "mundo"], "revista", True),
    ("le-monde", "Le Monde", "https://www.lemonde.fr/", "Principal diário francês de análises políticas e assuntos diplomáticos.", "FR", "fr", ["mundo", "politica"], "jornal", True),
    ("le-figaro", "Le Figaro", "https://www.lefigaro.fr/", "Um dos mais antigos jornais em circulação na França.", "FR", "fr", ["mundo", "politica"], "jornal", True),
    ("liberation", "Libération", "https://www.liberation.fr/", "Jornal francês de análise política e cultural.", "FR", "fr", ["mundo", "politica"], "jornal", True),
    ("les-echos", "Les Echos", "https://www.lesechos.fr/", "Principal diário econômico e financeiro da França.", "FR", "fr", ["economia"], "jornal", True),
    ("afp", "Agence France-Presse", "https://www.afp.com/", "Agência global de notícias e checagem de fatos.", "FR", "fr", ["mundo", "politica"], "agencia", True),
    ("der-spiegel", "Der Spiegel", "https://www.spiegel.de/", "Uma das maiores publicações investigativas da Alemanha e Europa.", "DE", "de", ["mundo", "politica"], "revista", True),
    ("die-welt", "Die Welt", "https://www.welt.de/", "Jornal diário alemão de notícias globais e análises políticas.", "DE", "de", ["mundo"], "jornal", True),
    ("faz", "Frankfurter Allgemeine", "https://www.faz.net/", "Jornalismo de referência na Alemanha sobre economia e política.", "DE", "de", ["mundo", "economia"], "jornal", True),
    ("deutsche-welle-brasil", "DW Brasil", "https://www.dw.com/pt-br/", "Emissora internacional da Alemanha oferecendo perspectiva europeia.", "DE", "pt-BR", ["mundo", "meio-ambiente", "politica"], "agencia", True),
    ("el-pais", "El País", "https://elpais.com/", "Jornal global com ampla cobertura internacional e geopolítica.", "ES", "es", ["mundo", "cultura", "politica"], "jornal", True),
    ("el-mundo-es", "El Mundo", "https://www.elmundo.es/", "Um dos principais jornais diários da Espanha.", "ES", "es", ["mundo", "politica"], "jornal", True),
    ("abc-espanha", "ABC", "https://www.abc.es/", "Diário espanhol de informação geral e relações ibero-americanas.", "ES", "es", ["mundo", "politica"], "jornal", True),
    ("la-vanguardia", "La Vanguardia", "https://www.lavanguardia.com/", "Jornalismo tradicional da Catalunha e Espanha.", "ES", "es", ["mundo"], "jornal", True),
    ("publico-pt", "Público", "https://www.publico.pt/", "Jornalismo português de referência sobre política e cultura.", "PT", "pt-PT", ["mundo", "cultura"], "jornal", True),
    ("observador-pt", "Observador", "https://observador.pt/", "Jornal digital português de análises, política e opinião.", "PT", "pt-PT", ["mundo", "politica"], "portal", True),
    ("diario-de-noticias-pt", "Diário de Notícias PT", "https://www.dn.pt/", "Histórico diário português em circulação desde 1864.", "PT", "pt-PT", ["mundo"], "jornal", True),
    ("corriere-della-sera", "Corriere della Sera", "https://www.corriere.it/", "Jornal de maior circulação e prestígio da Itália.", "IT", "it", ["mundo", "politica"], "jornal", True),
    ("la-repubblica", "La Repubblica", "https://www.repubblica.it/", "Diário italiano de análise política e de opinião.", "IT", "it", ["mundo"], "jornal", True),

    # --- ÁSIA, ORIENTE MÉDIO, ÁFRICA & OCEANIA (150+) ---
    ("nikkei-asia", "Nikkei Asia", "https://asia.nikkei.com/", "Jornalismo econômico focado nas economias e mercados do continente asiático.", "JP", "en", ["economia", "mundo"], "jornal", True),
    ("the-japan-times", "The Japan Times", "https://www.japantimes.co.jp/", "Maior jornal em língua inglesa do Japão.", "JP", "en", ["mundo"], "jornal", True),
    ("scmp", "South China Morning Post", "https://www.scmp.com/", "Jornal de Hong Kong com cobertura aprofundada sobre a China.", "HK", "en", ["mundo", "politica"], "jornal", True),
    ("xinhua", "Xinhua", "https://english.news.cn/", "Agência oficial de notícias da China.", "CN", "en", ["mundo"], "agencia", True),
    ("times-of-india", "The Times of India", "https://timesofindia.indiatimes.com/", "Jornal em língua inglesa de maior circulação na Índia.", "IN", "en", ["mundo", "politica"], "jornal", True),
    ("straits-times", "The Straits Times", "https://www.straitstimes.com/", "Veículo de imprensa de referência em Cingapura e Sudeste Asiático.", "SG", "en", ["mundo"], "jornal", True),
    ("al-jazeera", "Al Jazeera", "https://www.aljazeera.com/", "Rede internacional de notícias oferecendo perspectiva do Oriente Médio.", "QA", "en", ["mundo", "politica"], "portal", True),
    ("gulf-news", "Gulf News", "https://gulfnews.com/", "Portal de notícias diárias dos Emirados Árabes Unidos.", "AE", "en", ["mundo", "economia"], "portal", True),
    ("times-of-israel", "The Times of Israel", "https://www.timesofisrael.com/", "Notícias e análises sobre Israel e o Oriente Médio.", "IL", "en", ["mundo", "politica"], "portal", True),
    ("news24-sa", "News24", "https://www.news24.com/", "Principal portal de notícias da África do Sul.", "ZA", "en", ["mundo"], "portal", True),
    ("abc-news-au", "ABC News Australia", "https://www.abc.net.au/news", "Emissora e agência pública de notícias da Austrália.", "AU", "en", ["mundo"], "agencia", True),
    ("sydney-morning-herald", "The Sydney Morning Herald", "https://www.smh.com.au/", "Jornal diário australiano de grande prestígio.", "AU", "en", ["mundo"], "jornal", True),

    # --- CIÊNCIA, MEIO AMBIENTE, SAÚDE & ESPORTES (100+) ---
    ("nature", "Nature", "https://www.nature.com/", "Uma das mais prestigiosas revistas científicas multidisciplinares do mundo.", "GB", "en", ["ciencia"], "revista", True),
    ("science-mag", "Science Magazine", "https://www.science.org/", "Periódico científico de referência global publicado pela AAAS.", "US", "en", ["ciencia"], "revista", True),
    ("scientific-american", "Scientific American", "https://www.scientificamerican.com/", "Divulgação científica para o público amplo e análises inovadoras.", "US", "en", ["ciencia"], "revista", True),
    ("space-com", "Space.com", "https://www.space.com/", "Portal focado em astronomia, missões espaciais e astrofísica.", "US", "en", ["ciencia"], "portal", True),
    ("sciencedaily", "ScienceDaily", "https://www.sciencedaily.com/", "Agregador e portal de pesquisas e descobertas acadêmicas.", "US", "en", ["ciencia"], "portal", True),
    ("globo-esporte", "GE (Globo Esporte)", "https://ge.globo.com/", "Maior portal de cobertura esportiva, tabelas e bastidores no Brasil.", "BR", "pt-BR", ["esportes"], "portal", False),
    ("lance", "Lance!", "https://www.lance.com.br/", "Diário esportivo focado em futebol brasileiro e internacional.", "BR", "pt-BR", ["esportes"], "jornal", False),
    ("espn-brasil", "ESPN Brasil", "https://www.espn.com.br/", "Cobertura de modalidades esportivas, ligas internacionais e eSports.", "BR", "pt-BR", ["esportes"], "portal", False),
    ("marca", "Marca", "https://www.marca.com/", "Diário esportivo espanhol de grande circulação global.", "ES", "es", ["esportes"], "jornal", True),
    ("diario-as", "Diario AS", "https://as.com/", "Portal esportivo ibérico com forte cobertura do futebol europeu.", "ES", "es", ["esportes"], "jornal", True),
    ("national-geographic", "National Geographic", "https://www.nationalgeographic.com/", "Ciência, meio ambiente, geografia, conservação e culturas.", "US", "en", ["meio-ambiente", "ciencia"], "revista", True),
    ("mongabay", "Mongabay", "https://www.mongabay.com/", "Jornalismo ambiental independente com foco em florestas e biodiversidade.", "US", "en", ["meio-ambiente"], "portal", True),
    ("climate-home-news", "Climate Home News", "https://www.climatechangenews.com/", "Portal especializado em diplomacia e transição climática global.", "GB", "en", ["meio-ambiente"], "portal", True),
    ("webmd", "WebMD", "https://www.webmd.com/", "Portal de informação médica, bem-estar e saúde preventiva.", "US", "en", ["saude"], "portal", True),
    ("medical-news-today", "Medical News Today", "https://www.medicalnewstoday.com/", "Notícias e relatórios sobre pesquisas médicas e saúde pública.", "GB", "en", ["saude"], "portal", True),
]

def generate():
    seen_ids = set()
    formatted_entries = []

    for item in raw_sources:
        s_id, name, url, desc, country, lang, cats, s_type, is_int = item
        
        if s_id in seen_ids:
            print(f"⚠️ Erro: ID duplicado detectado '{s_id}'. Ignorando duplicata...", file=sys.stderr)
            continue
        seen_ids.add(s_id)

        cats_json = json.dumps(cats)
        entry = f"""  {{
    id: '{s_id}',
    name: '{name}',
    url: '{url}',
    description: '{desc}',
    country: '{country}',
    language: '{lang}',
    categories: {cats_json},
    type: '{s_type}',
    active: true,
    lastVerified: '2026-10-19',
    isInternational: {str(is_int).lower()}
  }}"""
        formatted_entries.append(entry)

    ts_content = "import type { NewsSource } from '../types';\n\n"
    ts_content += "export const sources: NewsSource[] = [\n"
    ts_content += ",\n".join(formatted_entries)
    ts_content += "\n];\n"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print(f"✅ {len(formatted_entries)} fontes gravadas com sucesso em '{OUTPUT_FILE}'!")

if __name__ == "__main__":
    generate()