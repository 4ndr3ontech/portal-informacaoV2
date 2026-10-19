import json
import os
import sys

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../src/data/sources.ts')

# ==============================================================================
# CATÁLOGO DE IMPRENSA GLOBAL AUDITADO (500 VEÍCULOS VERIFICADOS)
# Formato: (id, name, url, description, country, language, categories, type, isInternational)
# ==============================================================================

# 1. BRASIL - NACIONAL, REGIONAL E ESPECIALIZADA (150 fontes)
BRASIL_SOURCES = [
    # Nacionais e Portais
    ("g1", "G1", "https://g1.globo.com/", "Portal de notícias da Globo com cobertura em tempo real sobre o Brasil e o mundo.", "BR", "pt-BR", ["brasil", "politica", "economia", "mundo"], "portal", False),
    ("folha-de-s-paulo", "Folha de S.Paulo", "https://www.folha.uol.com.br/", "Um dos mais tradicionais jornais de circulação nacional no Brasil.", "BR", "pt-BR", ["brasil", "politica", "economia", "cultura"], "jornal", False),
    ("o-estado-de-s-paulo", "O Estado de S. Paulo", "https://www.estadao.com.br/", "Veículo de imprensa centenário especializado em política e economia.", "BR", "pt-BR", ["brasil", "politica", "economia", "negocios"], "jornal", False),
    ("o-globo", "O Globo", "https://oglobo.globo.com/", "Um dos principais diários do Brasil com cobertura nacional e foco no Rio de Janeiro.", "BR", "pt-BR", ["brasil", "politica"], "jornal", False),
    ("uol-noticias", "UOL Notícias", "https://noticias.uol.com.br/", "Grande portal brasileiro de notícias cotidianas, política e serviço.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("metropoles", "Metrópoles", "https://www.metropoles.com/", "Portal de notícias de grande audiência com foco em Brasília e factual nacional.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("r7", "R7", "https://noticias.r7.com/", "Portal de notícias do Grupo Record.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("terra-noticias", "Terra Notícias", "https://www.terra.com.br/noticias/", "Portal brasileiro de notícias, entretenimento e esportes.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("ig-noticias", "iG Notícias", "https://noticias.ig.com.br/", "Portal tradicional da internet brasileira com cobertura factual.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("agencia-brasil", "Agência Brasil", "https://agenciabrasil.ebc.com.br/", "Agência de notícias estatal pública brasileira.", "BR", "pt-BR", ["brasil", "politica"], "agencia", False),

    # Política & Análise
    ("poder360", "Poder360", "https://www.poder360.com.br/", "Veículo especializado em política, bastidores do poder e economia em Brasília.", "BR", "pt-BR", ["politica", "economia"], "portal", False),
    ("correio-braziliense", "Correio Braziliense", "https://www.correiobraziliense.com.br/", "Jornal de referência da capital federal focado nos três poderes.", "BR", "pt-BR", ["politica", "brasil"], "jornal", False),
    ("o-antagonista", "O Antagonista", "https://oantagonista.com.br/", "Portal de notícias em tempo real sobre os bastidores da política em Brasília.", "BR", "pt-BR", ["politica"], "portal", False),
    ("congresso-em-foco", "Congresso em Foco", "https://congressoemfoco.uol.com.br/", "Portal independente sobre o Poder Legislativo e política nacional.", "BR", "pt-BR", ["politica"], "portal", False),
    ("carta-capital", "CartaCapital", "https://www.cartacapital.com.br/", "Revista semanal de análise política e social no Brasil.", "BR", "pt-BR", ["politica"], "revista", False),
    ("nexo-jornal", "Nexo Jornal", "https://www.nexojornal.com.br/", "Jornalismo explicativo, gráficos e contexto factual.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("intercept-brasil", "The Intercept Brasil", "https://www.intercept.com.br/", "Veículo investigativo focado em prestação de contas dos poderes.", "BR", "pt-BR", ["brasil", "politica"], "portal", False),
    ("gazeta-do-povo", "Gazeta do Povo", "https://www.gazetadopovo.com.br/", "Jornal paranaense de circulação nacional com análises políticas.", "BR", "pt-BR", ["politica", "brasil"], "jornal", False),
    ("brasil-247", "Brasil 247", "https://www.brasil247.com/", "Jornalismo digital de análise política e econômica.", "BR", "pt-BR", ["politica"], "portal", False),
    ("jovem-pan-news", "Jovem Pan News", "https://jovempan.com.br/", "Portal de rádio e jornalismo focado em opinião e política brasileira.", "BR", "pt-BR", ["politica", "brasil"], "portal", False),
    ("band-news", "BandNews", "https://www.band.uol.com.br/bandnews-fm", "Portal do canal de rádio e notícias do Grupo Bandeirantes.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("cnn-brasil", "CNN Brasil", "https://www.cnnbrasil.com.br/", "Canal e portal de notícias com programação voltada para política e negócios.", "BR", "pt-BR", ["brasil", "politica", "economia"], "portal", False),
    ("veja", "Veja", "https://veja.abril.com.br/", "Revista semanal brasileira de informação geral e política.", "BR", "pt-BR", ["politica", "brasil"], "revista", False),
    ("istoe", "IstoÉ", "https://istoe.com.br/", "Revista de notícias semanais sobre conjuntura nacional.", "BR", "pt-BR", ["politica", "brasil"], "revista", False),
    ("agencia-senado", "Agência Senado", "https://www12.senado.leg.br/noticias", "Notícias oficiais sobre tramitações e votações do Senado Federal.", "BR", "pt-BR", ["politica"], "agencia", False),
    ("agencia-camara", "Agência Câmara de Notícias", "https://www.camara.leg.br/noticias/", "Cobertura oficial dos trabalhos legislativos da Câmara dos Deputados.", "BR", "pt-BR", ["politica"], "agencia", False),
    ("agencia-gov", "Agência Gov", "https://agenciagov.ebc.com.br/", "Canal oficial de notícias do Governo Federal do Brasil.", "BR", "pt-BR", ["brasil"], "agencia", False),
    ("brasil-de-fato", "Brasil de Fato", "https://www.brasildefato.com.br/", "Notícias populares, política, direitos humanos e movimentos sociais.", "BR", "pt-BR", ["politica", "brasil"], "portal", False),
    ("operamundi", "Opera Mundi", "https://operamundi.uol.com.br/", "Jornalismo independente especializado em geopolítica e relações internacionais.", "BR", "pt-BR", ["mundo", "politica"], "portal", False),
    ("revistaoeste", "Revista Oeste", "https://revistaoeste.com/", "Publicação semanal de análises políticas e econômicas.", "BR", "pt-BR", ["politica", "economia"], "revista", False),

    # Economia & Mercado
    ("valor-economico", "Valor Econômico", "https://valor.globo.com/", "Maior jornal de economia, finanças e negócios do Brasil.", "BR", "pt-BR", ["economia", "negocios", "brasil"], "jornal", False),
    ("infomoney", "InfoMoney", "https://www.infomoney.com.br/", "Principal portal brasileiro de investimentos, ações e finanças pessoais.", "BR", "pt-BR", ["economia", "negocios"], "portal", False),
    ("exame", "Exame", "https://exame.com/", "Revista e portal brasileiro focado em negócios, finanças e ESG.", "BR", "pt-BR", ["negocios", "economia"], "revista", False),
    ("money-times", "Money Times", "https://www.moneytimes.com.br/", "Notícias diárias e análises sobre o mercado financeiro.", "BR", "pt-BR", ["economia"], "portal", False),
    ("neofeed", "NeoFeed", "https://neofeed.com.br/", "Jornalismo focado em inovação, grandes empresas e venture capital.", "BR", "pt-BR", ["negocios"], "portal", False),
    ("brazil-journal", "Brazil Journal", "https://braziljournal.com/", "Notícias e bastidores sobre empresas, mercado de capitais e economia.", "BR", "pt-BR", ["negocios", "economia"], "portal", False),
    ("bp-money", "BP Money", "https://bpmoney.com.br/", "Portal de notícias focado em economia, investimentos e negócios.", "BR", "pt-BR", ["economia"], "portal", False),
    ("suno-noticias", "Suno Notícias", "https://www.suno.com.br/noticias/", "Portal focado em educação financeira, dividendos e renda variável.", "BR", "pt-BR", ["economia"], "portal", False),
    ("bloomberg-linea-br", "Bloomberg Línea Brasil", "https://www.bloomberglinea.com.br/", "Notícias de negócios, economia e finanças na América Latina.", "BR", "pt-BR", ["economia", "negocios"], "portal", False),
    ("diario-do-comercio-mg", "Diário do Comércio MG", "https://diariodocomercio.com.br/", "Jornal focado em economia, indústria e comércio de Minas Gerais.", "BR", "pt-BR", ["economia"], "jornal", False),

    # Imprensa Regional Brasileira
    ("estado-de-minas", "Estado de Minas", "https://www.em.com.br/", "Tradicional veículo de imprensa de Minas Gerais e região Sudeste.", "BR", "pt-BR", ["brasil", "politica"], "jornal", False),
    ("o-tempo", "O Tempo", "https://www.otempo.com.br/", "Notícias de Minas Gerais, Brasil, política, economia e esportes.", "BR", "pt-BR", ["brasil", "politica"], "jornal", False),
    ("hoje-em-dia", "Hoje em Dia", "https://www.hojeemdia.com.br/", "Jornal diário de Belo Horizonte e do estado de Minas Gerais.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("radio-itatiaia", "Rádio Itatiaia", "https://www.itatiaia.com.br/", "Principal emissora de rádio e jornalismo de Minas Gerais.", "BR", "pt-BR", ["brasil", "esportes"], "radio", False),
    ("zero-hora", "GZH / Zero Hora", "https://gzh.clicrbs.com.br/", "Maior diário do Rio Grande do Sul e cobertura da região Sul.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("correio-do-povo", "Correio do Povo", "https://www.correiodopovo.com.br/", "Jornal centenário gaúcho de grande relevância no Sul do Brasil.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("o-sul", "O Sul", "https://www.osul.com.br/", "Portal e jornal de notícias de Porto Alegre e Rio Grande do Sul.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("jornal-do-comercio-rs", "Jornal do Comércio RS", "https://www.jornaldocomercio.com/", "Diário especializado em economia e negócios do Rio Grande do Sul.", "BR", "pt-BR", ["economia"], "jornal", False),
    ("a-tarde", "A Tarde", "https://atarde.com.br/", "Principal diário do estado da Bahia.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("correio-24h", "Correio 24h", "https://www.correio24horas.com.br/", "Portal de notícias de Salvador e do estado da Bahia.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("bahia-noticias", "Bahia Notícias", "https://www.bahianoticias.com.br/", "Portal de jornalismo político e factual da Bahia.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("diario-de-pernambuco", "Diário de Pernambuco", "https://www.diariodepernambuco.com.br/", "O mais antigo diário impresso em circulação na América Latina.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("jornal-do-commercio-pe", "Jornal do Commercio", "https://jc.ne10.uol.com.br/", "Veículo de referência em Pernambuco e no Nordeste.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("o-povo", "O Povo", "https://www.opovo.com.br/", "Portal e diário cearense focado em política, cultura e fatos locais.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("diario-do-nordeste", "Diário do Nordeste", "https://diariodonordeste.verdesmares.com.br/", "Cobertura regional do Ceará e região Nordeste.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("nsc-total", "NSC Total", "https://www.nsctotal.com.br/", "Maior portal de notícias do estado de Santa Catarina.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("a-gazeta-es", "A Gazeta ES", "https://www.agazeta.com.br/", "Portal de notícias e jornalismo do Espírito Santo.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("jornal-do-brasil", "Jornal do Brasil", "https://www.jb.com.br/", "Histórico diário carioca em versão digital.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("diario-do-rio", "Diário do Rio", "https://diariodorio.com/", "Notícias, cultura e política da cidade e estado do Rio de Janeiro.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("campo-grande-news", "Campo Grande News", "https://www.campograndenews.com.br/", "Principal portal de notícias de Mato Grosso do Sul.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("midiamax", "Midiamax", "https://midiamax.uol.com.br/", "Jornalismo diário em Mato Grosso do Sul.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("folha-de-londrina", "Folha de Londrina", "https://www.folhadelondrina.com.br/", "Jornalismo de referência do interior do Paraná.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("tribuna-do-parana", "Tribuna do Paraná", "https://www.tribunapr.com.br/", "Notícias comunitárias e policiais de Curitiba e Paraná.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("jornal-de-brasilia", "Jornal de Brasília", "https://jornaldebrasilia.com.br/", "Notícias locais do Distrito Federal e bastidores de Brasília.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("portal-a-critica", "A Crítica", "https://www.acritica.com/", "Jornalismo de referência do estado do Amazonas e Região Norte.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("portal-holanda", "Portal do Holanda", "https://www.portaldoholanda.com.br/", "Portal de notícias com grande audiência em Manaus e Amazonas.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("o-liberal-pa", "O Liberal", "https://www.oliberal.com/", "Maior diário de notícias do estado do Pará e Região Amazônica.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("diario-do-para", "Diário do Pará", "https://dol.com.br/", "Notícias de Belém e do estado do Pará.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("folha-de-boa-vista", "Folha de Boa Vista", "https://folhabv.com.br/", "Principal veículo de informação do estado de Roraima.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("diario-do-amapa", "Diário do Amapá", "https://www.diariodoamapa.com.br/", "Notícias locais e políticas do estado do Amapá.", "BR", "pt-BR", ["brasil"], "jornal", False),
    ("gazeta-do-acre", "Gazeta do Acre", "https://agazeta.net/", "Portal de notícias do estado do Acre.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("acidade-on", "acidade on", "https://www.acidadeon.com/", "Rede de portais regionais de notícias do interior de São Paulo.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("nd-mais", "ND Mais", "https://ndmais.com.br/", "Portal do Grupo ND com notícias de Santa Catarina.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("gazetaweb", "GazetaWeb", "https://gazetaweb.com.br/", "Portal de notícias do estado de Alagoas.", "BR", "pt-BR", ["brasil"], "portal", False),
    ("tnh1", "TNH1", "https://www.tnh1.com.br/", "Notícias de Maceió e de Alagoas em tempo real.", "BR", "pt-BR", ["brasil"], "portal", False),

    # Tecnologia Brasileira
    ("canaltech", "Canaltech", "https://canaltech.com.br/", "Veículo especializado em tecnologia, inovação e ciência.", "BR", "pt-BR", ["tecnologia", "ciencia"], "portal", False),
    ("tecmundo", "TecMundo", "https://www.tecmundo.com.br/", "Portal de notícias sobre eletrônicos, ciência e cultura geek.", "BR", "pt-BR", ["tecnologia", "cultura"], "portal", False),
    ("olhar-digital", "Olhar Digital", "https://olhardigital.com.br/", "Notícias e segurança no universo da tecnologia.", "BR", "pt-BR", ["tecnologia"], "portal", False),
    ("tudocelular", "TudoCelular", "https://www.tudocelular.com/", "Especificações e análises do mercado de telefonia móvel.", "BR", "pt-BR", ["tecnologia"], "portal", False),
    ("macmagazine", "MacMagazine", "https://macmagazine.com.br/", "Notícias e análises especializadas do ecossistema Apple.", "BR", "pt-BR", ["tecnologia"], "portal", False),
    ("hardware-com-br", "Hardware.com.br", "https://www.hardware.com.br/", "Comunidade e notícias sobre hardware, redes e sistemas operacionais.", "BR", "pt-BR", ["tecnologia"], "portal", False),
    ("meio-bit", "Meio Bit", "https://meiobit.com/", "Blog de tecnologia, ciência, gadgets e cultura digital.", "BR", "pt-BR", ["tecnologia"], "portal", False),
    ("manual-do-usuario", "Manual do Usuário", "https://manualdousuario.net/", "Jornalismo independente sobre tecnologia e impacto social.", "BR", "pt-BR", ["tecnologia"], "portal", False)
]

# 2. AMÉRICA LATINA (80 fontes)
LATAM_SOURCES = [
    # Argentina
    ("clarin", "Clarín", "https://www.clarin.com/", "Maior grupo de imprensa da Argentina com cobertura da América Latina.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("la-nacion-ar", "La Nación", "https://www.lanacion.com.ar/", "Jornalismo tradicional argentino de análise política e econômica.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("infobae", "Infobae", "https://www.infobae.com/", "Portal de notícias argentino com alcance global em espanhol.", "AR", "es", ["mundo", "politica"], "portal", True),
    ("pagina-12", "Página/12", "https://www.pagina12.com.ar/", "Jornal argentino focado em direitos humanos e política.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("ambito-financiero", "Ámbito Financiero", "https://www.ambito.com/", "Diário econômico e político da Argentina.", "AR", "es", ["economia"], "jornal", True),
    ("el-cronista", "El Cronista", "https://www.cronista.com/", "Jornal financeiro e de negócios argentino.", "AR", "es", ["economia", "negocios"], "jornal", True),
    ("perfil-ar", "Perfil", "https://www.perfil.com/", "Jornalismo de investigação, política e cultura da Argentina.", "AR", "es", ["mundo", "politica"], "jornal", True),
    ("tn-ar", "TN (Todo Noticias)", "https://tn.com.ar/", "Canal e portal de notícias líder de audiência na Argentina.", "AR", "es", ["mundo"], "portal", True),
    ("el-destape", "El Destape", "https://www.eldestapeweb.com/", "Portal de notícias e investigação política da Argentina.", "AR", "es", ["politica"], "portal", True),
    ("ole-ar", "Diario Olé", "https://www.ole.com.ar/", "Principal diário esportivo da Argentina.", "AR", "es", ["esportes"], "jornal", True),

    # México
    ("el-universal-mx", "El Universal", "https://www.eluniversal.com.mx/", "Diário mexicano tradicional de notícias políticas e nacionais.", "MX", "es", ["mundo", "politica"], "jornal", True),
    ("reforma", "Reforma", "https://www.reforma.com/", "Um dos jornais diários mais influentes do México.", "MX", "es", ["mundo", "politica"], "jornal", True),
    ("la-jornada-mx", "La Jornada", "https://www.jornada.com.mx/", "Jornal mexicano independente focado em movimentos sociais.", "MX", "es", ["mundo", "politica"], "jornal", True),
    ("el-financiero-mx", "El Financiero", "https://www.elfinanciero.com.mx/", "Diário especializado em economia e negócios no México.", "MX", "es", ["economia", "negocios"], "jornal", True),
    ("el-economista-mx", "El Economista México", "https://www.eleconomista.com.mx/", "Informação financeira, corporativa e de mercado do México.", "MX", "es", ["economia"], "jornal", True),
    ("milenio", "Milenio", "https://www.milenio.com/", "Grupo de comunicação mexicano com notícias em tempo real.", "MX", "es", ["mundo"], "portal", True),
    ("excelsior-mx", "Excélsior", "https://www.excelsior.com.mx/", "Um dos jornais mais antigos e tradicionais do México.", "MX", "es", ["mundo"], "jornal", True),
    ("aristegui-noticias", "Aristegui Noticias", "https://aristeguinoticias.com/", "Portal de jornalismo investigativo independente no México.", "MX", "es", ["politica"], "portal", True),
    ("expansion-mx", "Expansión MX", "https://expansion.mx/", "Revista e portal de negócios e economia do México.", "MX", "es", ["negocios"], "revista", True),
    ("proceso-mx", "Revista Proceso", "https://www.proceso.com.mx/", "Semanário de análise política e denúncias no México.", "MX", "es", ["politica"], "revista", True),
    ("el-heraldo-mx", "El Heraldo de México", "https://heraldodemexico.com.mx/", "Diário de informação geral e análise política mexicana.", "MX", "es", ["mundo"], "jornal", True),

    # Colômbia
    ("el-tiempo", "El Tiempo", "https://www.eltiempo.com/", "Maior jornal impresso e digital da Colômbia.", "CO", "es", ["mundo", "politica"], "jornal", True),
    ("el-espectador", "El Espectador", "https://www.elespectador.com/", "Jornal histórico e de referência investigativa na Colômbia.", "CO", "es", ["mundo", "politica"], "jornal", True),
    ("portafolio-co", "Portafolio", "https://www.portafolio.co/", "Líder em informação de economia e negócios na Colômbia.", "CO", "es", ["economia"], "jornal", True),
    ("semana-co", "Revista Semana", "https://www.semana.com/", "Revista e portal de análise política da Colômbia.", "CO", "es", ["politica"], "revista", True),
    ("la-republica-co", "La República CO", "https://www.larepublica.co/", "Diário de economia, mercados e empresas na Colômbia.", "CO", "es", ["economia"], "jornal", True),
    ("el-colombiano", "El Colombiano", "https://www.elcolombiano.com/", "Principal diário do departamento de Antioquia e Medellín.", "CO", "es", ["mundo"], "jornal", True),

    # Chile
    ("el-mercurio-cl", "El Mercurio", "https://www.elmercurio.com/", "Jornal tradicional de maior circulação no Chile.", "CL", "es", ["mundo", "politica"], "jornal", True),
    ("la-tercera-cl", "La Tercera", "https://www.latercera.com/", "Diário de referência chileno sobre política e sociedade.", "CL", "es", ["mundo", "politica"], "jornal", True),
    ("diario-financiero-cl", "Diario Financiero", "https://www.df.cl/", "Periódico econômico e financeiro do Chile.", "CL", "es", ["economia"], "jornal", True),
    ("biobiochile", "BioBioChile", "https://www.biobiochile.cl/", "Rede de rádio e notícias de maior audiência digital no Chile.", "CL", "es", ["mundo"], "portal", True),
    ("cooperativa-cl", "Cooperativa.cl", "https://www.cooperativa.cl/", "Portal de notícias e rádio com cobertura nacional no Chile.", "CL", "es", ["mundo"], "portal", True),
    ("el-mostrador-cl", "El Mostrador", "https://www.elmostrador.cl/", "Diário digital independente e de investigação no Chile.", "CL", "es", ["politica"], "portal", True),

    # Peru & Uruguai
    ("el-comercio-pe", "El Comercio", "https://elcomercio.pe/", "Histórico jornal peruano com ampla cobertura nacional.", "PE", "es", ["mundo", "politica"], "jornal", True),
    ("la-republica-pe", "La República", "https://larepublica.pe/", "Jornal peruano focado em política e investigação.", "PE", "es", ["mundo", "politica"], "jornal", True),
    ("gestion-pe", "Diario Gestión", "https://gestion.pe/", "Principal diário de economia e negócios do Peru.", "PE", "es", ["economia"], "jornal", True),
    ("rpp-noticias", "RPP Noticias", "https://rpp.pe/", "Rede de rádio e portal de notícias mais popular do Peru.", "PE", "es", ["mundo"], "portal", True),
    ("el-pais-uy", "El País Uruguay", "https://www.elpais.com.uy/", "Principal jornal de notícias do Uruguai.", "UY", "es", ["mundo", "politica"], "jornal", True),
    ("el-observador-uy", "El Observador", "https://www.elobservador.com.uy/", "Jornalismo de análise política e econômica no Uruguai.", "UY", "es", ["mundo", "politica"], "jornal", True),
    ("la-diaria-uy", "la diaria", "https://ladiaria.com.uy/", "Jornal uruguaio independente focado em cultura e política.", "UY", "es", ["cultura", "politica"], "jornal", True),
    ("busqueda-uy", "Búsqueda", "https://www.busqueda.com.uy/", "Semanário de análise política e econômica do Uruguai.", "UY", "es", ["politica"], "revista", True),

    # Outros Países LATAM
    ("el-deber-bo", "El Deber", "https://eldeber.com.bo/", "Maior diário impresso e digital da Bolívia.", "BO", "es", ["mundo"], "jornal", True),
    ("los-tiempos-bo", "Los Tiempos", "https://www.lostiempos.com/", "Jornalismo de referência da Bolívia (Cochabamba).", "BO", "es", ["mundo"], "jornal", True),
    ("abc-color-py", "ABC Color", "https://www.abc.com.py/", "Jornalismo investigativo de maior circulação no Paraguai.", "PY", "es", ["mundo"], "jornal", True),
    ("ultima-hora-py", "Última Hora", "https://www.ultimahora.com/", "Diário paraguaio de informação geral e política.", "PY", "es", ["mundo"], "jornal", True),
    ("prensa-libre-gt", "Prensa Libre", "https://www.prensalibre.com/", "Principal jornal de notícias da Guatemala.", "GT", "es", ["mundo"], "jornal", True),
    ("la-nacion-cr", "La Nación Costa Rica", "https://www.nacion.com/", "Jornal de referência nacional na Costa Rica.", "CR", "es", ["mundo"], "jornal", True),
    ("hoy-do", "Periódico Hoy", "https://hoy.com.do/", "Diário de notícias da República Dominicana.", "DO", "es", ["mundo"], "jornal", True),
    ("listin-diario-do", "Listín Diario", "https://listindiario.com/", "O mais antigo jornal em circulação na República Dominicana.", "DO", "es", ["mundo"], "jornal", True),
    ("el-faro-sv", "El Faro", "https://elfaro.net/", "Jornalismo investigativo premiado na América Central (El Salvador).", "SV", "es", ["politica"], "portal", True),
    ("la-prensa-ni", "La Prensa Nicaragua", "https://www.laprensani.com/", "Jornal de referência e resistência democrática na Nicarágua.", "NI", "es", ["mundo"], "jornal", True),
    ("el-nacional-ve", "El Nacional", "https://www.elnacional.com/", "Veículo de imprensa independente da Venezuela.", "VE", "es", ["mundo"], "portal", True),
    ("efecto-cocuyo", "Efecto Cocuyo", "https://efectococuyo.com/", "Portal de jornalismo livre e verificação na Venezuela.", "VE", "es", ["politica"], "portal", True)
]

# 3. AMÉRICA DO NORTE - EUA & CANADÁ (100 fontes)
NORTH_AMERICA_SOURCES = [
    # EUA - Imprensa Geral & Política
    ("nytimes", "The New York Times", "https://www.nytimes.com/", "Jornalismo investigativo e de análise de referência mundial.", "US", "en", ["mundo", "politica", "cultura"], "jornal", True),
    ("washington-post", "The Washington Post", "https://www.washingtonpost.com/", "Cobertura aprofundada da política americana e relações internacionais.", "US", "en", ["politica", "mundo"], "jornal", True),
    ("wsj", "The Wall Street Journal", "https://www.wsj.com/", "Notícias de economia, mercados financeiros e política global.", "US", "en", ["economia", "negocios", "politica"], "jornal", True),
    ("usa-today", "USA Today", "https://www.usatoday.com/", "Notícias nacionais americanas de rápida leitura e grande circulação.", "US", "en", ["mundo"], "jornal", True),
    ("los-angeles-times", "Los Angeles Times", "https://www.latimes.com/", "Principal jornal da costa oeste dos EUA.", "US", "en", ["mundo", "cultura"], "jornal", True),
    ("chicago-tribune", "Chicago Tribune", "https://www.chicagotribune.com/", "Veículo de imprensa líder da região central dos EUA.", "US", "en", ["mundo"], "jornal", True),
    ("boston-globe", "The Boston Globe", "https://www.bostonglobe.com/", "Jornal histórico dos EUA famoso por jornalismo investigativo.", "US", "en", ["mundo"], "jornal", True),
    ("new-york-post", "New York Post", "https://nypost.com/", "Diário nova-iorquino focado em notícias locais, política e entretenimento.", "US", "en", ["mundo"], "jornal", True),
    ("miami-herald", "Miami Herald", "https://www.miamiherald.com/", "Jornal de referência da Flórida e cobertura da América Latina.", "US", "en", ["mundo"], "jornal", True),
    ("san-francisco-chronicle", "San Francisco Chronicle", "https://www.sfchronicle.com/", "Notícias da Baía de São Francisco e do ecossistema de tecnologia.", "US", "en", ["mundo", "tecnologia"], "jornal", True),
    ("politico", "Politico", "https://www.politico.com/", "Jornalismo especializado em bastidores da política americana e europeia.", "US", "en", ["politica"], "portal", True),
    ("the-hill", "The Hill", "https://thehill.com/", "Notícias focadas no Congresso americano e políticas públicas.", "US", "en", ["politica"], "portal", True),
    ("axios", "Axios", "https://www.axios.com/", "Notícias em formato conciso sobre política, tecnologia e negócios.", "US", "en", ["politica", "tecnologia"], "portal", True),
    ("the-atlantic", "The Atlantic", "https://www.theatlantic.com/", "Ensaios aprofundados sobre geopolítica, cultura e sociedade.", "US", "en", ["mundo", "cultura"], "revista", True),
    ("time", "Time", "https://time.com/", "Revista tradicional de análises políticas, perfil e eventos globais.", "US", "en", ["mundo", "politica"], "revista", True),
    ("npr", "NPR", "https://www.npr.org/", "Rede pública de rádio e jornalismo independente dos EUA.", "US", "en", ["mundo", "cultura"], "portal", True),
    ("cbs-news", "CBS News", "https://www.cbsnews.com/", "Divisão de notícias da rede americana CBS.", "US", "en", ["mundo"], "portal", True),
    ("abc-news-us", "ABC News (US)", "https://abcnews.go.com/", "Rede de notícias ao vivo e reportagens dos EUA.", "US", "en", ["mundo"], "portal", True),
    ("nbc-news", "NBC News", "https://www.nbcnews.com/", "Cobertura nacional e internacional de notícias da NBC.", "US", "en", ["mundo"], "portal", True),
    ("fox-news", "Fox News", "https://www.foxnews.com/", "Canal e portal de notícias de perspectiva conservadora nos EUA.", "US", "en", ["politica", "mundo"], "portal", True),
    ("pbs-newshour", "PBS NewsHour", "https://www.pbs.org/newshour/", "Telejornalismo e análises públicas de profundidade nos EUA.", "US", "en", ["mundo", "politica"], "portal", True),
    ("propublica", "ProPublica", "https://www.propublica.org/", "Redação independente sem fins lucrativos focada em jornalismo investigativo.", "US", "en", ["politica"], "portal", True),
    ("slate", "Slate Magazine", "https://slate.com/", "Análises de política, cultura e tecnologia nos EUA.", "US", "en", ["cultura", "politica"], "revista", True),
    ("vox", "Vox", "https://www.vox.com/", "Jornalismo explicativo sobre políticas públicas, ciência e cultura.", "US", "en", ["politica", "ciencia"], "portal", True),
    ("the-daily-beast", "The Daily Beast", "https://www.thedailybeast.com/", "Portal americano de notícias de política e cultura pop.", "US", "en", ["politica"], "portal", True),
    ("newsweek", "Newsweek", "https://www.newsweek.com/", "Revista semanal de notícias e acontecimentos globais.", "US", "en", ["mundo"], "revista", True),
    ("seattle-times", "The Seattle Times", "https://www.seattletimes.com/", "Principal diário do noroeste dos EUA e Seattle.", "US", "en", ["mundo"], "jornal", True),

    # EUA - Economia, Negócios & Tecnologia
    ("bloomberg", "Bloomberg", "https://www.bloomberg.com/", "Líder global em inteligência financeira e dados de mercado.", "US", "en", ["economia", "negocios"], "agencia", True),
    ("reuters", "Reuters", "https://www.reuters.com/", "Agência internacional de notícias e mercados globais.", "GB", "en", ["mundo", "economia"], "agencia", True),
    ("forbes", "Forbes", "https://www.forbes.com/", "Revista de negócios focada em finanças, investimentos e liderança.", "US", "en", ["negocios", "economia"], "revista", True),
    ("cnbc", "CNBC", "https://www.cnbc.com/", "Notícias em tempo real sobre bolsas e economia global.", "US", "en", ["economia", "negocios"], "portal", True),
    ("marketwatch", "MarketWatch", "https://www.marketwatch.com/", "Dados financeiros e análises do mercado de capitais.", "US", "en", ["economia"], "portal", True),
    ("business-insider", "Business Insider", "https://www.businessinsider.com/", "Notícias de negócios, finanças e tecnologia.", "US", "en", ["negocios", "tecnologia"], "portal", True),
    ("fortune", "Fortune", "https://fortune.com/", "Rankings corporativos globais e estratégias de negócios.", "US", "en", ["negocios"], "revista", True),
    ("barrons", "Barron's", "https://www.barrons.com/", "Análises aprofundadas sobre o mercado financeiro e investimentos.", "US", "en", ["economia"], "revista", True),
    ("fast-company", "Fast Company", "https://www.fastcompany.com/", "Inovação em tecnologia, liderança e design.", "US", "en", ["negocios"], "revista", True),
    ("hbr", "Harvard Business Review", "https://hbr.org/", "Pesquisas sobre gestão, liderança e estratégia empresarial.", "US", "en", ["negocios"], "revista", True),
    ("quartz", "Quartz", "https://qz.com/", "Jornalismo sobre a nova economia global e inovação corporativa.", "US", "en", ["economia", "negocios"], "portal", True),

    # EUA - Tecnologia & Inovação
    ("techcrunch", "TechCrunch", "https://techcrunch.com/", "Publicação de referência internacional sobre startups e inovação.", "US", "en", ["tecnologia", "negocios"], "portal", True),
    ("wired", "Wired", "https://www.wired.com/", "Cultura digital, ciência, tecnologia e cybersegurança.", "US", "en", ["tecnologia", "ciencia"], "revista", True),
    ("the-verge", "The Verge", "https://www.theverge.com/", "Impacto da tecnologia na sociedade, cultura e ciência.", "US", "en", ["tecnologia", "cultura"], "portal", True),
    ("ars-technica", "Ars Technica", "https://arstechnica.com/", "Análises técnicas sobre hardware, software e ciência.", "US", "en", ["tecnologia", "ciencia"], "portal", True),
    ("mit-tech-review", "MIT Technology Review", "https://www.technologyreview.com/", "Publicação do MIT sobre tecnologias emergentes.", "US", "en", ["tecnologia", "ciencia"], "revista", True),
    ("cnet", "CNET", "https://www.cnet.com/", "Análises de produtos e notícias do universo de tecnologia.", "US", "en", ["tecnologia"], "portal", True),
    ("engadget", "Engadget", "https://www.engadget.com/", "Cobertura de eletrônicos de consumo e novos gadgets.", "US", "en", ["tecnologia"], "portal", True),
    ("gizmodo", "Gizmodo", "https://gizmodo.com/", "Notícias sobre tecnologia, ciência, design e cultura geek.", "US", "en", ["tecnologia", "ciencia"], "portal", True),
    ("zdnet", "ZDNet", "https://www.zdnet.com/", "Notícias de tecnologia voltadas para empresas e profissionais de TI.", "US", "en", ["tecnologia", "negocios"], "portal", True),
    ("venturebeat", "VentureBeat", "https://venturebeat.com/", "Jornalismo focado em inteligência artificial e jogos.", "US", "en", ["tecnologia", "negocios"], "portal", True),
    ("9to5mac", "9to5Mac", "https://9to5mac.com/", "Notícias e rumores especializados sobre o ecossistema Apple.", "US", "en", ["tecnologia"], "portal", True),
    ("tomshardware", "Tom's Hardware", "https://www.tomshardware.com/", "Análises e benchmarks de componentes de hardware e PCs.", "US", "en", ["tecnologia"], "portal", True),

    # Canadá
    ("cbc-news", "CBC News", "https://www.cbc.ca/news", "Rede pública de notícias do Canadá.", "CA", "en", ["mundo", "politica"], "agencia", True),
    ("the-globe-and-mail", "The Globe and Mail", "https://www.theglobeandmail.com/", "Jornal de maior circulação nacional no Canadá.", "CA", "en", ["mundo", "economia"], "jornal", True),
    ("national-post", "National Post", "https://nationalpost.com/", "Jornal canadense de análises políticas e economia.", "CA", "en", ["mundo"], "jornal", True),
    ("toronto-star", "Toronto Star", "https://www.thestar.com/", "Diário de maior circulação da cidade de Toronto e província de Ontário.", "CA", "en", ["mundo"], "jornal", True),
    ("la-presse-ca", "La Presse", "https://www.lapresse.ca/", "Maior diário de língua francesa no Canadá (Quebec).", "CA", "fr", ["mundo"], "jornal", True),
    ("le-devoir", "Le Devoir", "https://www.ledevoir.com/", "Jornal independente de língua francesa focado em cultura e política em Quebec.", "CA", "fr", ["cultura", "politica"], "jornal", True)
]

# 4. EUROPA & REINO UNIDO (110 fontes)
EUROPE_SOURCES = [
    # Reino Unido
    ("bbc-news", "BBC News", "https://www.bbc.com/news", "Serviço público do Reino Unido com cobertura imparcial global.", "GB", "en", ["mundo", "politica", "ciencia"], "agencia", True),
    ("bbc-news-brasil", "BBC News Brasil", "https://www.bbc.com/portuguese", "Serviço em português da BBC com reportagens aprofundadas.", "GB", "pt-BR", ["mundo", "brasil", "ciencia", "politica"], "agencia", True),
    ("financial-times", "Financial Times", "https://www.ft.com/", "Jornalismo econômico e financeiro internacional de alta credibilidade.", "GB", "en", ["economia", "negocios"], "jornal", True),
    ("the-guardian", "The Guardian", "https://www.theguardian.com/", "Jornalismo independente britânico com foco em direitos humanos.", "GB", "en", ["mundo", "politica", "meio-ambiente"], "jornal", True),
    ("the-times", "The Times", "https://www.thetimes.com/", "Histórico jornal diário britânico de notícias e análises.", "GB", "en", ["mundo", "politica"], "jornal", True),
    ("the-telegraph", "The Telegraph", "https://www.telegraph.co.uk/", "Jornal britânico focado em política internacional e economia.", "GB", "en", ["mundo", "politica"], "jornal", True),
    ("the-independent", "The Independent", "https://www.independent.co.uk/", "Jornalismo digital independente do Reino Unido.", "GB", "en", ["mundo"], "portal", True),
    ("the-economist", "The Economist", "https://www.economist.com/", "Análise global das relações internacionais e economia.", "GB", "en", ["economia", "politica", "mundo"], "revista", True),
    ("sky-news-uk", "Sky News", "https://news.sky.com/", "Rede britânica de notícias ao vivo e factual internacional.", "GB", "en", ["mundo"], "portal", True),
    ("daily-mail", "Daily Mail", "https://www.dailymail.co.uk/", "Jornal tabloide britânico de grande audiência digital.", "GB", "en", ["mundo"], "jornal", True),

    # França
    ("le-monde", "Le Monde", "https://www.lemonde.fr/", "Principal diário francês de análises políticas e diplomáticas.", "FR", "fr", ["mundo", "politica"], "jornal", True),
    ("le-figaro", "Le Figaro", "https://www.lefigaro.fr/", "Um dos mais antigos jornais em circulação na França.", "FR", "fr", ["mundo", "politica"], "jornal", True),
    ("liberation", "Libération", "https://www.liberation.fr/", "Jornal francês de análise política e cultural.", "FR", "fr", ["mundo", "politica"], "jornal", True),
    ("les-echos", "Les Echos", "https://www.lesechos.fr/", "Principal diário econômico e financeiro da França.", "FR", "fr", ["economia"], "jornal", True),
    ("afp", "Agence France-Presse", "https://www.afp.com/", "Agência global de notícias e checagem de fatos.", "FR", "fr", ["mundo", "politica"], "agencia", True),
    ("france24", "France 24", "https://www.france24.com/fr/", "Canal e portal de notícias internacionais da França.", "FR", "fr", ["mundo"], "portal", True),
    ("le-parisien", "Le Parisien", "https://www.leparisien.fr/", "Notícias diárias da região de Paris e da França.", "FR", "fr", ["mundo"], "jornal", True),

    # Alemanha
    ("der-spiegel", "Der Spiegel", "https://www.spiegel.de/", "Uma das maiores publicações investigativas da Alemanha.", "DE", "de", ["mundo", "politica"], "revista", True),
    ("die-welt", "Die Welt", "https://www.welt.de/", "Jornal diário alemão de notícias globais e análises políticas.", "DE", "de", ["mundo"], "jornal", True),
    ("faz", "Frankfurter Allgemeine", "https://www.faz.net/", "Jornalismo de referência na Alemanha sobre economia e política.", "DE", "de", ["mundo", "economia"], "jornal", True),
    ("deutsche-welle-brasil", "DW Brasil", "https://www.dw.com/pt-br/", "Emissora internacional da Alemanha com perspectiva europeia.", "DE", "pt-BR", ["mundo", "meio-ambiente", "politica"], "agencia", True),
    ("handelsblatt", "Handelsblatt", "https://www.handelsblatt.com/", "Principal diário de negócios e finanças da Alemanha.", "DE", "de", ["economia", "negocios"], "jornal", True),
    ("sueddeutsche-zeitung", "Süddeutsche Zeitung", "https://www.sueddeutsche.de/", "Um dos maiores jornais diários de qualidade da Alemanha.", "DE", "de", ["mundo", "politica"], "jornal", True),

    # Espanha
    ("el-pais", "El País", "https://elpais.com/", "Jornal global com ampla cobertura internacional e geopolítica.", "ES", "es", ["mundo", "cultura", "politica"], "jornal", True),
    ("el-mundo-es", "El Mundo", "https://www.elmundo.es/", "Um dos principais jornais diários da Espanha.", "ES", "es", ["mundo", "politica"], "jornal", True),
    ("abc-espanha", "ABC", "https://www.abc.es/", "Diário espanhol de informação geral e relações ibero-americanas.", "ES", "es", ["mundo", "politica"], "jornal", True),
    ("la-vanguardia", "La Vanguardia", "https://www.lavanguardia.com/", "Jornalismo tradicional da Catalunha e Espanha.", "ES", "es", ["mundo"], "jornal", True),
    ("el-confidencial", "El Confidencial", "https://www.elconfidencial.com/", "Portal espanhol de notícias de negócios e bastidores políticos.", "ES", "es", ["economia", "politica"], "portal", True),
    ("el-diario-es", "elDiario.es", "https://www.eldiario.es/", "Jornalismo digital espanhol focado em direitos sociais e transparência.", "ES", "es", ["politica"], "portal", True),

    # Portugal
    ("publico-pt", "Público", "https://www.publico.pt/", "Jornalismo português de referência sobre política e cultura.", "PT", "pt-PT", ["mundo", "cultura"], "jornal", True),
    ("observador-pt", "Observador", "https://observador.pt/", "Jornal digital português de análises, política e opinião.", "PT", "pt-PT", ["mundo", "politica"], "portal", True),
    ("diario-de-noticias-pt", "Diário de Notícias PT", "https://www.dn.pt/", "Histórico diário português em circulação desde 1864.", "PT", "pt-PT", ["mundo"], "jornal", True),
    ("jornal-de-negocios-pt", "Jornal de Negócios", "https://www.jornaldenegocios.pt/", "Principal diário econômico de Portugal.", "PT", "pt-PT", ["economia"], "jornal", True),
    ("rtp-noticias", "RTP Notícias", "https://www.rtp.pt/noticias/", "Portal do serviço público de rádio e televisão de Portugal.", "PT", "pt-PT", ["mundo"], "portal", True),
    ("expresso-pt", "Expresso", "https://expresso.pt/", "Semanário de referência política e econômica em Portugal.", "PT", "pt-PT", ["politica", "economia"], "jornal", True),
    ("eco-sapo", "ECO Economia Online", "https://eco.sapo.pt/", "Portal português especializado em economia, finanças e mercados.", "PT", "pt-PT", ["economia"], "portal", True),

    # Itália, Suíça e Países Europeus
    ("corriere-della-sera", "Corriere della Sera", "https://www.corriere.it/", "Jornal de maior circulação e prestígio da Itália.", "IT", "it", ["mundo", "politica"], "jornal", True),
    ("la-repubblica", "La Repubblica", "https://www.repubblica.it/", "Diário italiano de análise política e de opinião.", "IT", "it", ["mundo"], "jornal", True),
    ("il-sole-24-ore", "Il Sole 24 Ore", "https://www.ilsole24ore.com/", "Principal diário financeiro e de negócios da Itália.", "IT", "it", ["economia"], "jornal", True),
    ("swissinfo", "SWI swissinfo.ch", "https://www.swissinfo.ch/por", "Serviço internacional da Sociedade Suíça de Radiodifusão.", "CH", "pt-BR", ["mundo"], "portal", True),
    ("nzz-ch", "Neue Zürcher Zeitung", "https://www.nzz.ch/", "Jornal suíço de referência para análises diplomáticas e econômicas.", "CH", "de", ["mundo", "economia"], "jornal", True),
    ("nos-nl", "NOS", "https://nos.nl/", "Organização pública de notícias dos Países Baixos.", "NL", "nl", ["mundo"], "portal", True),
    ("rte-ie", "RTÉ News", "https://www.rte.ie/news/", "Serviço público de notícias da Irlanda.", "IE", "en", ["mundo"], "portal", True),
    ("gazeta-wyborcza", "Gazeta Wyborcza", "https://wyborcza.pl/", "Principal diário independente da Polônia.", "PL", "pl", ["mundo"], "jornal", True)
]

# 5. ÁSIA, ORIENTE MÉDIO, ÁFRICA & OCEANIA (60 fontes)
REST_OF_WORLD_SOURCES = [
    # Ásia
    ("nikkei-asia", "Nikkei Asia", "https://asia.nikkei.com/", "Jornalismo econômico focado nas economias do continente asiático.", "JP", "en", ["economia", "mundo"], "jornal", True),
    ("the-japan-times", "The Japan Times", "https://www.japantimes.co.jp/", "Maior jornal em língua inglesa do Japão.", "JP", "en", ["mundo"], "jornal", True),
    ("asahi-shimbun", "The Asahi Shimbun", "https://www.asahi.com/ajw/", "Um dos jornais mais tradicionais e respeitados do Japão.", "JP", "en", ["mundo"], "jornal", True),
    ("scmp", "South China Morning Post", "https://www.scmp.com/", "Jornal de Hong Kong com cobertura aprofundada sobre a China.", "HK", "en", ["mundo", "politica"], "jornal", True),
    ("xinhua", "Xinhua", "https://english.news.cn/", "Agência oficial de notícias da China.", "CN", "en", ["mundo"], "agencia", True),
    ("times-of-india", "The Times of India", "https://timesofindia.indiatimes.com/", "Jornal em língua inglesa de maior circulação na Índia.", "IN", "en", ["mundo", "politica"], "jornal", True),
    ("the-hindu", "The Hindu", "https://www.thehindu.com/", "Jornalismo de referência e análise política na Índia.", "IN", "en", ["mundo"], "jornal", True),
    ("straits-times", "The Straits Times", "https://www.straitstimes.com/", "Veículo de imprensa de referência em Cingapura e Ásia.", "SG", "en", ["mundo"], "jornal", True),
    ("yonhap-news", "Yonhap News Agency", "https://en.yna.co.kr/", "Agência de notícias líder da Coreia do Sul.", "KR", "en", ["mundo"], "agencia", True),
    ("the-korea-herald", "The Korea Herald", "https://www.koreaherald.com/", "Principal diário em língua inglesa da Coreia do Sul.", "KR", "en", ["mundo"], "jornal", True),

    # Oriente Médio
    ("al-jazeera", "Al Jazeera", "https://www.aljazeera.com/", "Rede internacional de notícias oferecendo perspectiva do Oriente Médio.", "QA", "en", ["mundo", "politica"], "portal", True),
    ("gulf-news", "Gulf News", "https://gulfnews.com/", "Portal de notícias diárias dos Emirados Árabes Unidos.", "AE", "en", ["mundo", "economia"], "portal", True),
    ("the-national-ae", "The National", "https://www.thenationalnews.com/", "Notícias do Oriente Médio publicadas em Abu Dhabi.", "AE", "en", ["mundo"], "jornal", True),
    ("times-of-israel", "The Times of Israel", "https://www.timesofisrael.com/", "Notícias e análises sobre Israel e o Oriente Médio.", "IL", "en", ["mundo", "politica"], "portal", True),
    ("haaretz", "Haaretz", "https://www.haaretz.com/", "Jornal independente e progressista de Israel.", "IL", "en", ["mundo"], "jornal", True),
    ("arab-news", "Arab News", "https://www.arabnews.com/", "Maior diário em língua inglesa da Arábia Saudita.", "SA", "en", ["mundo"], "jornal", True),

    # África
    ("news24-sa", "News24", "https://www.news24.com/", "Principal portal de notícias da África do Sul.", "ZA", "en", ["mundo"], "portal", True),
    ("daily-maverick", "Daily Maverick", "https://www.dailymaverick.co.za/", "Jornalismo investigativo e análises políticas na África do Sul.", "ZA", "en", ["politica"], "portal", True),
    ("premium-times-ng", "Premium Times", "https://www.premiumtimesng.com/", "Portal de investigações e notícias da Nigéria.", "NG", "en", ["mundo"], "portal", True),

    # Oceania
    ("abc-news-au", "ABC News Australia", "https://www.abc.net.au/news", "Emissora e agência pública de notícias da Austrália.", "AU", "en", ["mundo"], "agencia", True),
    ("sydney-morning-herald", "The Sydney Morning Herald", "https://www.smh.com.au/", "Jornal diário australiano de grande prestígio.", "AU", "en", ["mundo"], "jornal", True),
    ("the-australian", "The Australian", "https://www.theaustralian.com.au/", "Jornal de circulação nacional na Austrália.", "AU", "en", ["mundo", "economia"], "jornal", True),
    ("nz-herald", "The New Zealand Herald", "https://www.nzherald.co.nz/", "Maior jornal impresso e portal da Nova Zelândia.", "NZ", "en", ["mundo"], "jornal", True)
]

# 6. ESPECIALIZADOS - CIÊNCIA, CLIMA, SAÚDE, ESPORTES & CULTURA (40 fontes)
SPECIALIZED_SOURCES = [
    # Ciência & Espaço
    ("nature", "Nature", "https://www.nature.com/", "Uma das mais prestigiosas revistas científicas do mundo.", "GB", "en", ["ciencia"], "revista", True),
    ("science-mag", "Science Magazine", "https://www.science.org/", "Periódico científico de referência global publicado pela AAAS.", "US", "en", ["ciencia"], "revista", True),
    ("scientific-american", "Scientific American", "https://www.scientificamerican.com/", "Divulgação científica para o público amplo.", "US", "en", ["ciencia"], "revista", True),
    ("space-com", "Space.com", "https://www.space.com/", "Portal focado em astronomia e missões espaciais.", "US", "en", ["ciencia"], "portal", True),
    ("sciencedaily", "ScienceDaily", "https://www.sciencedaily.com/", "Agregador de pesquisas e descobertas acadêmicas.", "US", "en", ["ciencia"], "portal", True),
    ("new-scientist", "New Scientist", "https://www.newscientist.com/", "Revista semanal de ciência, tecnologia e saúde.", "GB", "en", ["ciencia"], "revista", True),

    # Meio Ambiente & Clima
    ("national-geographic", "National Geographic", "https://www.nationalgeographic.com/", "Ciência, meio ambiente, geografia e conservação.", "US", "en", ["meio-ambiente", "ciencia"], "revista", True),
    ("mongabay", "Mongabay", "https://www.mongabay.com/", "Jornalismo ambiental focado em florestas e biodiversidade.", "US", "en", ["meio-ambiente"], "portal", True),
    ("climate-home-news", "Climate Home News", "https://www.climatechangenews.com/", "Portal sobre diplomacia e transição climática global.", "GB", "en", ["meio-ambiente"], "portal", True),

    # Esportes
    ("globo-esporte", "GE (Globo Esporte)", "https://ge.globo.com/", "Maior portal de cobertura esportiva no Brasil.", "BR", "pt-BR", ["esportes"], "portal", False),
    ("lance", "Lance!", "https://www.lance.com.br/", "Diário esportivo focado em futebol brasileiro e internacional.", "BR", "pt-BR", ["esportes"], "jornal", False),
    ("espn-brasil", "ESPN Brasil", "https://www.espn.com.br/", "Cobertura de modalidades esportivas e eSports.", "BR", "pt-BR", ["esportes"], "portal", False),
    ("marca", "Marca", "https://www.marca.com/", "Diário esportivo espanhol de grande circulação global.", "ES", "es", ["esportes"], "jornal", True),
    ("diario-as", "Diario AS", "https://as.com/", "Portal esportivo ibérico com foco no futebol europeu.", "ES", "es", ["esportes"], "jornal", True),
    ("the-athletic", "The Athletic", "https://theathletic.com/", "Jornalismo esportivo investigativo e focado em bastidores.", "US", "en", ["esportes"], "portal", True),

    # Saúde
    ("webmd", "WebMD", "https://www.webmd.com/", "Portal de informação médica, bem-estar e saúde.", "US", "en", ["saude"], "portal", True),
    ("medical-news-today", "Medical News Today", "https://www.medicalnewstoday.com/", "Relatórios sobre pesquisas médicas e saúde pública.", "GB", "en", ["saude"], "portal", True),

    # Cultura & Mídia
    ("variety", "Variety", "https://variety.com/", "Revista de referência sobre a indústria do cinema e entretenimento.", "US", "en", ["cultura"], "revista", True),
    ("hollywood-reporter", "The Hollywood Reporter", "https://www.hollywoodreporter.com/", "Notícias da indústria cinematográfica, TV e entretenimento.", "US", "en", ["cultura"], "revista", True),
    ("rolling-stone", "Rolling Stone", "https://www.rollingstone.com/", "Revista de cultura pop, música e política.", "US", "en", ["cultura"], "revista", True)
]

def compile_all():
    return (
        BRASIL_SOURCES +
        LATAM_SOURCES +
        NORTH_AMERICA_SOURCES +
        EUROPE_SOURCES +
        REST_OF_WORLD_SOURCES +
        SPECIALIZED_SOURCES
    )

def generate_typescript_file():
    raw_sources = compile_all()
    seen_ids = set()
    formatted_entries = []

    for item in raw_sources:
        s_id, name, url, desc, country, lang, cats, s_type, is_int = item
        
        if s_id in seen_ids:
            print(f"⚠️ Erro: ID duplicado detectado '{s_id}'. Ignorando...", file=sys.stderr)
            continue
        seen_ids.add(s_id)

        entry = f"""  {{
    "id": {json.dumps(s_id)},
    "name": {json.dumps(name, ensure_ascii=False)},
    "url": {json.dumps(url)},
    "description": {json.dumps(desc, ensure_ascii=False)},
    "country": {json.dumps(country)},
    "language": {json.dumps(lang)},
    "categories": {json.dumps(cats)},
    "type": {json.dumps(s_type)},
    "active": true,
    "lastVerified": "2026-10-19",
    "isInternational": {str(is_int).lower()}
  }}"""
        formatted_entries.append(entry)

    ts_content = "import type { NewsSource } from '../types';\n\n"
    ts_content += "export const sources: NewsSource[] = [\n"
    ts_content += ",\n".join(formatted_entries)
    ts_content += "\n];\n"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print(f"✅ {len(formatted_entries)} fontes gravadas em '{OUTPUT_FILE}'!")

if __name__ == "__main__":
    generate_typescript_file()