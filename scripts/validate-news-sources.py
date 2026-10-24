import json
import os

# Caminho do arquivo JSON gerado
DATA_FILE = 'data/news-sources.json'
ESPERADO = 5000

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Arquivo {DATA_FILE} não encontrado.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    ids = set(item.get('id') for item in data)
    urls = set(item.get('url') for item in data)

    print("\n--- RELATÓRIO DE VALIDAÇÃO ---")
    print(f"Total coletado: {total}")
    print(f"IDs Únicos: {len(ids)}")
    print(f"URLs Únicas: {len(urls)}")

    problemas = []
    
    # Atualizado para exigir 5000 sites
    if total != ESPERADO:
        problemas.append(f"Quantidade incorreta: Encontrados {total} de {ESPERADO} esperados.")
        
    if len(ids) != total:
        problemas.append("Alerta: Existem IDs duplicados.")
        
    if len(urls) != total:
        problemas.append("Alerta: Existem URLs duplicadas.")

    if problemas:
        print("\nProblemas encontrados:")
        for p in problemas:
            print(f"- {p}")
    else:
        print("\n✅ APROVADO SEM ERROS")

if __name__ == "__main__":
    main()