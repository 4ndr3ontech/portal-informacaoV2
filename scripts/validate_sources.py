import json
import re
import sys
from pathlib import Path

SOURCES_FILE = Path(__file__).parent.parent / "src" / "data" / "sources.ts"

VALID_CATEGORIES = {
    "brasil", "politica", "economia", "mundo", "cultura",
    "negocios", "tecnologia", "ciencia", "esportes", "meio-ambiente", "saude"
}

VALID_TYPES = {"portal", "jornal", "revista", "agencia", "tv", "radio"}
COUNTRY_REGEX = re.compile(r"^[A-Z]{2}$")
LANG_REGEX = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")
URL_REGEX = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")

def run_audit():
    print("🔍 Iniciando auditoria do catálogo em 'src/data/sources.ts'...\n")

    if not SOURCES_FILE.exists():
        print(f"❌ Erro Crítico: Arquivo {SOURCES_FILE} não encontrado.")
        sys.exit(1)

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Localiza o inicio do array apos a atribuicao '= [' para ignorar o tipo 'NewsSource[]'
    assign_idx = content.find("= [")
    if assign_idx == -1:
        print("❌ Erro Crítico: Declaração 'export const sources... = [' não encontrada.")
        sys.exit(1)

    start_idx = content.find("[", assign_idx)
    end_idx = content.rfind("]")
    if start_idx == -1 or end_idx == -1:
        print("❌ Erro Crítico: Não foi possível delimitar o array de fontes.")
        sys.exit(1)

    json_str = content[start_idx : end_idx + 1]

    try:
        sources = json.loads(json_str)
    except Exception as e:
        print(f"❌ Erro ao decodificar JSON das fontes: {e}")
        sys.exit(1)

    total_records = len(sources)
    print(f"📊 Total de registros encontrados: {total_records} / 1.000")

    seen_ids = set()
    seen_urls = set()
    errors = []
    warnings = []

    for index, src in enumerate(sources, 1):
        s_id = src.get("id")
        name = src.get("name")
        url = src.get("url")
        country = src.get("country")
        lang = src.get("language")
        categories = src.get("categories", [])
        s_type = src.get("type")

        # 1. Checagem de ID
        if not s_id:
            errors.append(f"Registro #{index}: ID ausente.")
        elif s_id in seen_ids:
            errors.append(f"Registro #{index}: ID duplicado '{s_id}'.")
        else:
            seen_ids.add(s_id)

        # 2. Checagem de URL
        if not url:
            errors.append(f"[{s_id}] URL ausente.")
        elif url in seen_urls:
            warnings.append(f"[{s_id}] URL duplicada detectada: '{url}'.")
        elif not URL_REGEX.match(url):
            errors.append(f"[{s_id}] URL malformada ou sem protocolo: '{url}'.")
        else:
            seen_urls.add(url)

        # 3. Código de País (ISO Alpha-2)
        if not country or not COUNTRY_REGEX.match(country):
            errors.append(f"[{s_id}] Código de país inválido: '{country}'. Use ISO 3166-1 alpha-2 (ex: 'BR').")

        # 4. Idioma (IETF BCP 47)
        if not lang or not LANG_REGEX.match(lang):
            errors.append(f"[{s_id}] Código de idioma inválido: '{lang}'. Ex: 'pt-BR' ou 'en'.")

        # 5. Categorias
        if not categories or not isinstance(categories, list):
            errors.append(f"[{s_id}] Categorias devem ser uma lista não vazia.")
        else:
            for cat in categories:
                if cat not in VALID_CATEGORIES:
                    errors.append(f"[{s_id}] Categoria não reconhecida: '{cat}'.")

        # 6. Tipo de Veículo
        if s_type not in VALID_TYPES:
            errors.append(f"[{s_id}] Tipo de veículo inválido: '{s_type}'.")

    # Relatório Final
    print("\n--- RELATÓRIO DE DIAGNÓSTICO ---")
    if warnings:
        print(f"\n⚠️ AVISOS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n❌ ERROS ENCONTRADOS ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
        print("\n❌ APROVAÇÃO: REPROVADO. Corrija os erros acima.")
        sys.exit(1)
    else:
        print("\n✅ VALIDAÇÃO TÉCNICA: APROVADO sem erros de sintaxe ou schema!")
        if total_records == 1000:
            print("🎉 META ALCANÇADA: Catálogo completo com exatamente 1.000 fontes verificadas!")
        else:
            print(f"ℹ️ STATUS DE CURADORIA: {total_records} fontes validadas. Faltam {1000 - total_records} fontes para a meta final.")

if __name__ == "__main__":
    run_audit()