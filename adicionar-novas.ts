import fs from 'fs/promises';
import type { NewsSource } from './src/types';

// A sua nova lista de 100 sites
const novasFontes: NewsSource[] = [
  { id: "atribuna", name: "A Tribuna", url: "https://www.atribuna.com.br", country: "BR", categories: ["politica", "economia", "esportes"], description: "Jornalismo regional de Santos, litoral paulista e Baixada Santista.", rank: 372, score: "87", audience: "Medium", active: true },
  { id: "diariodolitoral", name: "Diário do Litoral", url: "https://www.diariodolitoral.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias da Baixada Santista e litoral de São Paulo.", rank: 373, score: "80", audience: "Medium", active: true },
  { id: "diariodeuberlandia", name: "Diário de Uberlândia", url: "https://diariodeuberlandia.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias de Uberlândia e do Triângulo Mineiro.", rank: 374, score: "78", audience: "Medium", active: true },
  { id: "correiodeuberlandia", name: "Correio de Uberlândia", url: "https://www.correiodeuberlandia.com.br", country: "BR", categories: ["politica", "economia"], description: "Cobertura jornalística do Triângulo Mineiro.", rank: 375, score: "74", audience: "Low", active: true },
  { id: "jornaldeuberaba", name: "Jornal de Uberaba", url: "https://www.jornaldeuberaba.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias e acontecimentos de Uberaba e região.", rank: 376, score: "73", audience: "Low", active: true },
  { id: "gazetadocerrado", name: "Gazeta do Cerrado", url: "https://gazetadocerrado.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias do Tocantins e da região Norte.", rank: 377, score: "78", audience: "Medium", active: true },
  { id: "conexaoto", name: "Conexão Tocantins", url: "https://conexaoto.com.br", country: "BR", categories: ["politica", "economia"], description: "Jornalismo político e regional do Tocantins.", rank: 378, score: "77", audience: "Medium", active: true },
  { id: "t1noticias", name: "T1 Notícias", url: "https://www.t1noticias.com.br", country: "BR", categories: ["politica", "economia"], description: "Portal de notícias de Palmas e do Tocantins.", rank: 379, score: "78", audience: "Medium", active: true },
  { id: "jornaldotocantins", name: "Jornal do Tocantins", url: "https://www.jornaldotocantins.com.br", country: "BR", categories: ["politica", "economia"], description: "Cobertura de acontecimentos e política tocantinense.", rank: 380, score: "76", audience: "Low", active: true },
  { id: "gazetadopovo-pr", name: "Plural", url: "https://www.plural.jor.br", country: "BR", categories: ["politica", "economia"], description: "Jornalismo independente com foco em Curitiba e Paraná.", rank: 381, score: "81", audience: "Medium", active: true },
  { id: "paranaportal", name: "Paraná Portal", url: "https://www.paranaportal.com", country: "BR", categories: ["politica", "economia"], description: "Notícias de Curitiba e do estado do Paraná.", rank: 382, score: "80", audience: "Medium", active: true },
  { id: "ricmais", name: "RIC Mais", url: "https://ric.com.br", country: "BR", categories: ["politica", "economia", "esportes"], description: "Portal de notícias e conteúdo regional do Paraná.", rank: 383, score: "86", audience: "Medium", active: true },
  { id: "diariodaregiao", name: "Diário da Região", url: "https://www.diariodaregiao.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias de São José do Rio Preto e região.", rank: 384, score: "83", audience: "Medium", active: true },
  { id: "acidadeon-araraquara", name: "ACidade ON Araraquara", url: "https://www.acidadeon.com/araraquara", country: "BR", categories: ["politica", "economia"], description: "Cobertura regional de Araraquara e interior paulista.", rank: 385, score: "77", audience: "Medium", active: true },
  { id: "acidadeon-sao-carlos", name: "ACidade ON São Carlos", url: "https://www.acidadeon.com/saocarlos", country: "BR", categories: ["politica", "economia"], description: "Notícias de São Carlos e região.", rank: 386, score: "76", audience: "Medium", active: true },
  { id: "jornalacidade", name: "Jornal A Cidade", url: "https://www.jornalacidade.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias regionais e acontecimentos do interior paulista.", rank: 387, score: "73", audience: "Low", active: true },
  { id: "diariodepernambuco-regional", name: "Marco Zero", url: "https://marcozero.org", country: "BR", categories: ["politica", "economia", "ciencia"], description: "Jornalismo independente e investigativo de Pernambuco.", rank: 388, score: "84", audience: "Medium", active: true },
  { id: "agenciasertao", name: "Agência Sertão", url: "https://agenciasertao.com", country: "BR", categories: ["politica", "economia"], description: "Notícias do interior da Bahia e do semiárido brasileiro.", rank: 389, score: "78", audience: "Medium", active: true },
  { id: "portalr10", name: "R10 Notícias", url: "https://r10noticias.com", country: "BR", categories: ["politica", "economia"], description: "Cobertura de acontecimentos regionais e notícias do Nordeste.", rank: 390, score: "70", audience: "Low", active: true },
  { id: "diariodocentrooeste", name: "Diário do Centro-Oeste", url: "https://www.diariodoaco.com.br", country: "BR", categories: ["politica", "economia"], description: "Cobertura regional e acontecimentos do interior brasileiro.", rank: 391, score: "65", audience: "Low", active: true },
  { id: "itforum", name: "IT Forum", url: "https://itforum.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Notícias sobre tecnologia corporativa, inovação e transformação digital.", rank: 392, score: "89", audience: "Medium", active: true },
  { id: "computerworldbrasil", name: "Computerworld Brasil", url: "https://computerworld.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Jornalismo sobre tecnologia empresarial e infraestrutura de TI.", rank: 393, score: "88", audience: "Medium", active: true },
  { id: "cio", name: "CIO", url: "https://cio.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Tecnologia da informação, gestão e liderança digital.", rank: 394, score: "87", audience: "Medium", active: true },
  { id: "inforchannel", name: "InforChannel", url: "https://inforchannel.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Notícias sobre canais de tecnologia, software e infraestrutura.", rank: 395, score: "82", audience: "Medium", active: true },
  { id: "ipnews", name: "IPNews", url: "https://ipnews.com.br", country: "BR", categories: ["tecnologia"], description: "Informações sobre tecnologia, telecomunicações e segurança digital.", rank: 396, score: "79", audience: "Medium", active: true },
  { id: "securityreport", name: "Security Report", url: "https://securityreport.com.br", country: "BR", categories: ["tecnologia"], description: "Notícias sobre cibersegurança, proteção de dados e ameaças digitais.", rank: 397, score: "84", audience: "Medium", active: true },
  { id: "cryptoid", name: "Crypto ID", url: "https://cryptoid.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Identidade digital, certificação, criptografia e segurança da informação.", rank: 398, score: "78", audience: "Low", active: true },
  { id: "mundopositivo", name: "Mundo Positivo", url: "https://www.mundopositivo.com.br", country: "BR", categories: ["tecnologia", "entretenimento"], description: "Conteúdos digitais, tecnologia e atualidades.", rank: 399, score: "75", audience: "Low", active: true },
  { id: "tecnologiaig", name: "iG Tecnologia", url: "https://www.ig.com.br", country: "BR", categories: ["tecnologia"], description: "Conteúdo de tecnologia e novidades do universo digital.", rank: 400, score: "85", audience: "High", active: true },
  { id: "baguete-ti", name: "Baguete Tecnologia", url: "https://www.baguete.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Notícias sobre tecnologia empresarial e mercado de TI.", rank: 401, score: "80", audience: "Medium", active: true },
  { id: "cienciahoje", name: "Ciência Hoje", url: "https://cienciahoje.org.br", country: "BR", categories: ["ciencia"], description: "Divulgação científica e reportagens sobre pesquisas brasileiras.", rank: 402, score: "91", audience: "Medium", active: true },
  { id: "comciencia", name: "ComCiência", url: "https://www.comciencia.br", country: "BR", categories: ["ciencia", "tecnologia"], description: "Revista eletrônica de jornalismo científico e divulgação científica.", rank: 403, score: "86", audience: "Medium", active: true },
  { id: "pesquisafapesp", name: "Pesquisa FAPESP", url: "https://revistapesquisa.fapesp.br", country: "BR", categories: ["ciencia", "saude"], description: "Reportagens aprofundadas sobre ciência, pesquisa e inovação.", rank: 404, score: "96", audience: "High", active: true },
  { id: "abc-ciencia", name: "Academia Brasileira de Ciências", url: "https://www.abc.org.br", country: "BR", categories: ["ciencia"], description: "Informações sobre pesquisas, cientistas e desenvolvimento científico.", rank: 405, score: "90", audience: "Medium", active: true },
  { id: "sbpc", name: "SBPC", url: "https://portal.sbpcnet.org.br", country: "BR", categories: ["ciencia", "educacao"], description: "Sociedade Brasileira para o Progresso da Ciência e divulgação científica.", rank: 406, score: "88", audience: "Medium", active: true },
  { id: "agencia-mcti", name: "Ministério da Ciência e Tecnologia", url: "https://www.gov.br/mcti", country: "BR", categories: ["ciencia", "tecnologia"], description: "Informações oficiais sobre ciência, tecnologia e inovação no Brasil.", rank: 407, score: "95", audience: "High", active: true },
  { id: "instituto-butantan", name: "Instituto Butantan", url: "https://butantan.gov.br", country: "BR", categories: ["ciencia", "saude"], description: "Pesquisa científica, vacinas, saúde pública e biotecnologia.", rank: 408, score: "94", audience: "High", active: true },
  { id: "inpe", name: "INPE", url: "https://www.gov.br/inpe", country: "BR", categories: ["ciencia", "tecnologia"], description: "Pesquisas espaciais, monitoramento ambiental e meteorologia.", rank: 409, score: "95", audience: "High", active: true },
  { id: "embrapa", name: "Embrapa", url: "https://www.embrapa.br", country: "BR", categories: ["ciencia", "economia"], description: "Pesquisa agropecuária, inovação e desenvolvimento tecnológico no campo.", rank: 410, score: "97", audience: "High", active: true },
  { id: "museudavida", name: "Museu da Vida Fiocruz", url: "https://museudavida.fiocruz.br", country: "BR", categories: ["ciencia", "saude"], description: "Divulgação científica, educação e cultura em saúde.", rank: 411, score: "80", audience: "Medium", active: true },
  { id: "vivabem", name: "VivaBem UOL", url: "https://www.uol.com.br/vivabem", country: "BR", categories: ["saude"], description: "Notícias e informações sobre saúde, alimentação e qualidade de vida.", rank: 412, score: "94", audience: "High", active: true },
  { id: "saudeabril", name: "Saúde Abril", url: "https://saude.abril.com.br", country: "BR", categories: ["saude", "ciencia"], description: "Jornalismo especializado em saúde, medicina e prevenção.", rank: 413, score: "93", audience: "High", active: true },
  { id: "dicasdemulher", name: "Dicas de Mulher", url: "https://www.dicasdemulher.com.br", country: "BR", categories: ["saude", "entretenimento"], description: "Conteúdo sobre saúde, bem-estar e qualidade de vida.", rank: 414, score: "85", audience: "Medium", active: true },
  { id: "portalhospitaisbrasil", name: "Hospitais Brasil", url: "https://portalhospitaisbrasil.com.br", country: "BR", categories: ["saude", "economia"], description: "Notícias sobre hospitais, medicina e gestão de saúde.", rank: 415, score: "80", audience: "Medium", active: true },
  { id: "medscape-br", name: "Medscape Brasil", url: "https://portugues.medscape.com", country: "BR", categories: ["saude", "ciencia"], description: "Informações médicas, pesquisas e atualizações científicas.", rank: 416, score: "88", audience: "Medium", active: true },
  { id: "valorinveste", name: "Valor Investe", url: "https://valorinveste.globo.com", country: "BR", categories: ["economia"], description: "Notícias sobre investimentos, finanças pessoais e mercado financeiro.", rank: 417, score: "95", audience: "High", active: true },
  { id: "finsiders", name: "Finsiders", url: "https://finsiders.com.br", country: "BR", categories: ["economia", "tecnologia"], description: "Jornalismo sobre fintechs, inovação financeira e meios de pagamento.", rank: 418, score: "82", audience: "Medium", active: true },
  { id: "startse", name: "StartSe", url: "https://www.startse.com", country: "BR", categories: ["economia", "tecnologia"], description: "Inovação, empreendedorismo e transformação dos negócios.", rank: 419, score: "90", audience: "High", active: true },
  { id: "empreendedor", name: "Empreendedor", url: "https://empreendedor.com.br", country: "BR", categories: ["economia"], description: "Conteúdo sobre empreendedorismo, empresas e gestão.", rank: 420, score: "81", audience: "Medium", active: true },
  { id: "administradores", name: "Administradores", url: "https://administradores.com.br", country: "BR", categories: ["economia"], description: "Gestão, administração, carreira e negócios.", rank: 421, score: "88", audience: "Medium", active: true },
  { id: "contabeis", name: "Portal Contábeis", url: "https://www.contabeis.com.br", country: "BR", categories: ["economia"], description: "Notícias tributárias, contabilidade, legislação e negócios.", rank: 422, score: "89", audience: "Medium", active: true },
  { id: "jornalcontabil", name: "Jornal Contábil", url: "https://www.jornalcontabil.com.br", country: "BR", categories: ["economia"], description: "Informações sobre economia, tributos, trabalho e contabilidade.", rank: 423, score: "84", audience: "Medium", active: true },
  { id: "diariodocomercio", name: "Diário do Comércio", url: "https://diariodocomercio.com.br", country: "BR", categories: ["economia"], description: "Notícias sobre economia, comércio e empreendedorismo.", rank: 424, score: "84", audience: "Medium", active: true },
  { id: "agrolink", name: "Agrolink", url: "https://www.agrolink.com.br", country: "BR", categories: ["economia", "ciencia"], description: "Notícias, mercado agrícola, cotações e tecnologia no agronegócio.", rank: 425, score: "91", audience: "High", active: true },
  { id: "noticiasagricolas", name: "Notícias Agrícolas", url: "https://www.noticiasagricolas.com.br", country: "BR", categories: ["economia"], description: "Notícias, cotações e informações sobre o mercado agropecuário.", rank: 426, score: "94", audience: "High", active: true },
  { id: "agrolinknoticias", name: "AgroLink Notícias", url: "https://www.agrolink.com.br/noticias", country: "BR", categories: ["economia", "ciencia"], description: "Atualizações sobre agricultura, pecuária e mercado rural.", rank: 427, score: "86", audience: "Medium", active: true },
  { id: "revistacultivar", name: "Revista Cultivar", url: "https://revistacultivar.com.br", country: "BR", categories: ["economia", "ciencia"], description: "Tecnologia agrícola, máquinas, equipamentos e produção rural.", rank: 428, score: "84", audience: "Medium", active: true },
  { id: "canalagro", name: "Canal Agro", url: "https://canalagro.ebc.com.br", country: "BR", categories: ["economia", "ciencia"], description: "Conteúdo sobre agricultura, pecuária e desenvolvimento rural.", rank: 429, score: "82", audience: "Medium", active: true },
  { id: "oeco", name: " ((o))eco", url: "https://oeco.org.br", country: "BR", categories: ["ciencia", "politica"], description: "Jornalismo ambiental, conservação e biodiversidade.", rank: 430, score: "89", audience: "Medium", active: true },
  { id: "olympics-br", name: "Time Brasil", url: "https://www.cob.org.br", country: "BR", categories: ["esportes"], description: "Notícias oficiais do Comitê Olímpico do Brasil.", rank: 431, score: "91", audience: "High", active: true },
  { id: "cbf", name: "CBF", url: "https://www.cbf.com.br", country: "BR", categories: ["esportes"], description: "Notícias oficiais do futebol brasileiro e seleções nacionais.", rank: 432, score: "96", audience: "High", active: true },
  { id: "olimpiadatododia", name: "Olimpíada Todo Dia", url: "https://www.olimpiadatododia.com.br", country: "BR", categories: ["esportes"], description: "Cobertura de esportes olímpicos e atletas brasileiros.", rank: 433, score: "85", audience: "Medium", active: true },
  { id: "surto", name: "Surto Olímpico", url: "https://surtoolimpico.com.br", country: "BR", categories: ["esportes"], description: "Notícias e resultados de modalidades olímpicas.", rank: 434, score: "81", audience: "Medium", active: true },
  { id: "tenisbrasil", name: "Tênis Brasil", url: "https://tenisbrasil.uol.com.br", country: "BR", categories: ["esportes"], description: "Notícias, resultados e análises do tênis nacional e internacional.", rank: 435, score: "83", audience: "Medium", active: true },
  { id: "volei", name: "Vôlei Brasil", url: "https://cbv.com.br", country: "BR", categories: ["esportes"], description: "Informações oficiais do voleibol brasileiro.", rank: 436, score: "88", audience: "Medium", active: true },
  { id: "futsalbrasil", name: "CBFS", url: "https://cbfs.com.br", country: "BR", categories: ["esportes"], description: "Notícias oficiais e informações sobre futsal brasileiro.", rank: 437, score: "82", audience: "Medium", active: true },
  { id: "fogaonet", name: "FogãoNET", url: "https://www.fogaonet.com", country: "BR", categories: ["esportes"], description: "Notícias e cobertura dedicada ao Botafogo.", rank: 438, score: "85", audience: "Medium", active: true },
  { id: "meuflu", name: "Explosão Tricolor", url: "https://explosaotricolor.com.br", country: "BR", categories: ["esportes"], description: "Notícias e análises sobre o Fluminense.", rank: 439, score: "80", audience: "Medium", active: true },
  { id: "cruzeirosempre", name: "Cruzeiro Sports", url: "https://cruzeirosports.com.br", country: "BR", categories: ["esportes"], description: "Cobertura e notícias sobre o Cruzeiro Esporte Clube.", rank: 440, score: "76", audience: "Low", active: true },
  { id: "adorocinema", name: "AdoroCinema", url: "https://www.adorocinema.com", country: "BR", categories: ["entretenimento"], description: "Notícias, críticas, trailers e lançamentos de cinema e séries.", rank: 441, score: "94", audience: "High", active: true },
  { id: "cinemacomrapadura", name: "Cinema com Rapadura", url: "https://cinemacomrapadura.com.br", country: "BR", categories: ["entretenimento"], description: "Jornalismo, críticas e novidades sobre cinema e audiovisual.", rank: 442, score: "85", audience: "Medium", active: true },
  { id: "cinepop", name: "CinePOP", url: "https://cinepop.com.br", country: "BR", categories: ["entretenimento"], description: "Notícias sobre filmes, séries, televisão e cultura pop.", rank: 443, score: "87", audience: "Medium", active: true },
  { id: "tracklist", name: "Tracklist", url: "https://tracklist.com.br", country: "BR", categories: ["entretenimento"], description: "Notícias sobre música, artistas, festivais e cultura pop.", rank: 444, score: "86", audience: "Medium", active: true },
  { id: "tenhomaisdiscos", name: "Tenho Mais Discos Que Amigos!", url: "https://www.tenhomaisdiscosqueamigos.com", country: "BR", categories: ["entretenimento"], description: "Jornalismo musical, lançamentos e cultura independente.", rank: 445, score: "83", audience: "Medium", active: true },
  { id: "musicjournal", name: "Music Journal", url: "https://www.musicjournal.com.br", country: "BR", categories: ["entretenimento"], description: "Notícias sobre música, artistas e indústria fonográfica.", rank: 446, score: "78", audience: "Medium", active: true },
  { id: "observatoriodatv", name: "Observatório da TV", url: "https://observatoriodatv.com.br", country: "BR", categories: ["entretenimento"], description: "Notícias sobre televisão, novelas, audiência e celebridades.", rank: 447, score: "89", audience: "High", active: true },
  { id: "natelinha", name: "NaTelinha", url: "https://natelinha.uol.com.br", country: "BR", categories: ["entretenimento"], description: "Cobertura de televisão, novelas, streaming e entretenimento.", rank: 448, score: "88", audience: "High", active: true },
  { id: "rd1", name: "RD1", url: "https://rd1.com.br", country: "BR", categories: ["entretenimento"], description: "Notícias sobre televisão, famosos e entretenimento.", rank: 449, score: "84", audience: "Medium", active: true },
  { id: "tvpop", name: "TV Pop", url: "https://www.tvpop.com.br", country: "BR", categories: ["entretenimento"], description: "Jornalismo sobre televisão, audiência e bastidores da mídia.", rank: 450, score: "83", audience: "Medium", active: true },
  { id: "autopapo", name: "AutoPapo", url: "https://autopapo.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Notícias, dicas automotivas, manutenção e mercado de veículos.", rank: 451, score: "89", audience: "Medium", active: true },
  { id: "motociclismo", name: "Motociclismo Online", url: "https://motociclismoonline.com.br", country: "BR", categories: ["tecnologia"], description: "Notícias, avaliações e lançamentos do mercado de motocicletas.", rank: 452, score: "82", audience: "Medium", active: true },
  { id: "motorsportbr", name: "Motorsport Brasil", url: "https://motorsport.uol.com.br", country: "BR", categories: ["esportes", "tecnologia"], description: "Notícias e cobertura do automobilismo nacional e internacional.", rank: 453, score: "92", audience: "High", active: true },
  { id: "autossegredos", name: "Autos Segredos", url: "https://www.autossegredos.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Informações sobre lançamentos, indústria automotiva e novos veículos.", rank: 454, score: "84", audience: "Medium", active: true },
  { id: "insideevsbr", name: "InsideEVs Brasil", url: "https://insideevs.uol.com.br", country: "BR", categories: ["tecnologia", "economia"], description: "Notícias sobre carros elétricos, baterias e mobilidade sustentável.", rank: 455, score: "86", audience: "Medium", active: true },
  { id: "melhoresdestinos", name: "Melhores Destinos", url: "https://www.melhoresdestinos.com.br", country: "BR", categories: ["entretenimento", "economia"], description: "Notícias de viagens, turismo, passagens e destinos.", rank: 456, score: "96", audience: "High", active: true },
  { id: "viajenaviagem", name: "Viaje na Viagem", url: "https://www.viajenaviagem.com", country: "BR", categories: ["entretenimento"], description: "Guias de viagem, destinos turísticos e planejamento de roteiros.", rank: 457, score: "89", audience: "Medium", active: true },
  { id: "panrotas", name: "PANROTAS", url: "https://www.panrotas.com.br", country: "BR", categories: ["economia", "entretenimento"], description: "Jornalismo especializado em turismo e indústria de viagens.", rank: 458, score: "87", audience: "Medium", active: true },
  { id: "mercadoeeventos", name: "Mercado & Eventos", url: "https://www.mercadoeeventos.com.br", country: "BR", categories: ["economia", "entretenimento"], description: "Notícias sobre turismo, hotelaria, eventos e viagens.", rank: 459, score: "84", audience: "Medium", active: true },
  { id: "ambientebrasil", name: "Ambiente Brasil", url: "https://ambientes.ambientebrasil.com.br", country: "BR", categories: ["ciencia"], description: "Informações sobre meio ambiente, sustentabilidade e conservação.", rank: 460, score: "80", audience: "Medium", active: true },
  { id: "fontesegura", name: "Fonte Segura", url: "https://fontesegura.forumseguranca.org.br", country: "BR", categories: ["politica"], description: "Jornalismo e análises especializadas em segurança pública.", rank: 461, score: "86", audience: "Medium", active: true },
  { id: "forumseguranca", name: "Fórum Brasileiro de Segurança Pública", url: "https://forumseguranca.org.br", country: "BR", categories: ["politica", "ciencia"], description: "Estudos, pesquisas e dados sobre segurança pública no Brasil.", rank: 462, score: "92", audience: "Medium", active: true },
  { id: "justicaglobal", name: "Justiça Global", url: "https://www.global.org.br", country: "BR", categories: ["politica"], description: "Informações sobre direitos humanos e justiça.", rank: 463, score: "80", audience: "Low", active: true },
  { id: "ibccrim", name: "IBCCRIM", url: "https://ibccrim.org.br", country: "BR", categories: ["politica", "ciencia"], description: "Conteúdo jurídico e estudos sobre ciências criminais.", rank: 464, score: "86", audience: "Medium", active: true },
  { id: "direitonews", name: "Direito News", url: "https://www.direitonews.com.br", country: "BR", categories: ["politica"], description: "Notícias, legislação e atualidades do universo jurídico.", rank: 465, score: "76", audience: "Low", active: true },
  { id: "jcconcursos", name: "JC Concursos", url: "https://jcconcursos.com.br", country: "BR", categories: ["economia"], description: "Notícias sobre concursos públicos, editais e oportunidades profissionais.", rank: 466, score: "92", audience: "High", active: true },
  { id: "folha-dirigida", name: "Folha Dirigida", url: "https://folha.qconcursos.com", country: "BR", categories: ["economia"], description: "Notícias e informações sobre concursos e carreiras públicas.", rank: 467, score: "90", audience: "High", active: true },
  { id: "qconcursos", name: "Qconcursos", url: "https://www.qconcursos.com", country: "BR", categories: ["educacao", "economia"], description: "Educação, preparação para concursos e carreira profissional.", rank: 468, score: "92", audience: "High", active: true },
  { id: "guiadacarreira", name: "Guia da Carreira", url: "https://www.guiadacarreira.com.br", country: "BR", categories: ["educacao", "economia"], description: "Orientação profissional, cursos e formação acadêmica.", rank: 469, score: "85", audience: "Medium", active: true },
  { id: "portaltrt", name: "Justiça do Trabalho", url: "https://www.tst.jus.br", country: "BR", categories: ["politica", "economia"], description: "Notícias oficiais sobre legislação trabalhista e decisões judiciais.", rank: 470, score: "97", audience: "High", active: true },
  { id: "govbrnoticias", name: "Agência Gov", url: "https://agenciagov.ebc.com.br", country: "BR", categories: ["politica", "economia"], description: "Notícias oficiais sobre políticas públicas e ações do governo federal.", rank: 471, score: "96", audience: "High", active: true }
];

async function extrairDescricaoReal(url: string) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 6000);

    const resposta = await fetch(url, {
      headers: { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' 
      },
      signal: controller.signal
    });
    clearTimeout(timeout);

    if (!resposta.ok) return null;

    const html = await resposta.text();
    const regexDescricao = /<meta[^>]+(?:name|property)=["'](?:og:)?description["'][^>]+content=["']([^"']+)["']/i;
    const regexAlternativa = /<meta[^>]+content=["']([^"']+)["'][^>]+(?:name|property)=["'](?:og:)?description["']/i;

    const match = html.match(regexDescricao) || html.match(regexAlternativa);
    return match ? match[1].replace(/(\r\n|\n|\r)/gm, " ").trim() : null;
  } catch (erro) {
    return null;
  }
}

async function iniciarProcesso() {
  const caminhoFicheiro = './src/data/fontes-brasil.json';
  
  console.log('A ler a base atual de sites enriquecidos...');
  const dadosAtuais = JSON.parse(await fs.readFile(caminhoFicheiro, 'utf-8'));
  
  console.log(`Processando ${novasFontes.length} novas fontes...`);
  let atualizados = 0;

  for (let i = 0; i < novasFontes.length; i++) {
    const site = novasFontes[i];
    console.log(`[${i+1}/${novasFontes.length}] A extrair: ${site.name}...`);
    
    const descricaoReal = await extrairDescricaoReal(site.url);
    
    if (descricaoReal && descricaoReal.length > 10) {
      site.description = descricaoReal;
      (site as any).fullDescription = descricaoReal; 
      atualizados++;
      console.log(`   ✅ Encontrada: ${descricaoReal.substring(0, 80)}...`);
    } else {
      console.log(`   ❌ Nenhuma descrição extraída. Mantendo a original.`);
    }
    
    // Adiciona o site à base existente
    dadosAtuais.push(site);
    
    await new Promise(r => setTimeout(r, 1000));
  }

  // Grava o arquivo novamente
  await fs.writeFile(caminhoFicheiro, JSON.stringify(dadosAtuais, null, 2));
  
  console.log(`\n🎉 Concluído! ${atualizados} novas fontes tiveram suas descrições reais extraídas.`);
  console.log('👉 As 100 fontes foram adicionadas com sucesso ao arquivo fontes-brasil.json!');
}

iniciarProcesso();