import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'news-sources.json')
TARGET_COUNT = 1000

def validate():
    if not os.path.exists(DATA_FILE):
        print(f"ERRO: Arquivo {DATA_FILE} não encontrado.")
        sys.exit(1)

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    errors = []
    ids = set()
    urls = set()
    ranks = []

    count = len(data)
    if count != TARGET_COUNT:
        errors.append(f"Quantidade incorreta: Encontrados {count} de {TARGET_COUNT} esperados.")

    for i, record in enumerate(data):
        # Campos obrigatórios
        if not record.get('id'): errors.append(f"Registro {i}: ID ausente")
        if not record.get('name'): errors.append(f"Registro {i} ({record.get('id')}): Nome ausente")
        if not record.get('url') or not record.get('url').startswith('http'): 
            errors.append(f"Registro {i} ({record.get('name')}): URL inválida ({record.get('url')})")
        
        # Duplicidades
        if record['id'] in ids: errors.append(f"ID Duplicado: {record['id']}")
        ids.add(record['id'])
        
        if record['url'] in urls: errors.append(f"URL Duplicada: {record['url']}")
        urls.add(record['url'])

        # Rank
        if record.get('rank') is not None:
            ranks.append(record['rank'])

    # Valida ordenação do Rank
    if ranks != sorted(ranks):
        errors.append("Aviso: A ordenação do rank não está estritamente sequencial/crescente.")

    print(f"\n--- RELATÓRIO DE VALIDAÇÃO ---")
    print(f"Total coletado: {count}")
    print(f"IDs Únicos: {len(ids)}")
    print(f"URLs Únicas: {len(urls)}")
    
    if errors:
        print("\nProblemas encontrados:")
        for err in errors[:20]:
            print(f"- {err}")
        if len(errors) > 20:
            print(f"...e mais {len(errors) - 20} erros.")
        sys.exit(1)
    else:
        print("\n✅ Validação concluída com sucesso. Catálogo pronto para produção.")
        sys.exit(0)

if __name__ == "__main__":
    validate()