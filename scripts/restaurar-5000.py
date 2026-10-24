import json
import os

JSON_PATH = 'data/news-sources.json'
TS_PATH = 'src/data/sources.ts'

def main():
    if not os.path.exists(JSON_PATH):
        print(f"Erro: O ficheiro {JSON_PATH} não foi encontrado.")
        return

    # Lê os 5000 sites do JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        fontes = json.load(f)

    # Escreve os 5000 sites no TypeScript usando o tipo NewsSource
    ts_content = "import type { NewsSource } from '../types';\n\nexport const sources: NewsSource[] = "
    ts_content += json.dumps(fontes, ensure_ascii=False, indent=2)
    ts_content += ";\n"

    with open(TS_PATH, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    print(f"✅ Sucesso! {len(fontes)} sites foram injetados no ficheiro {TS_PATH}.")

if __name__ == "__main__":
    main()