import sqlite3
import csv

# Caminho para o banco
db_path = './src/app/code_smells.db'

# Conexão
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Colunas da tabela
colunas_code_smells = [
    "smell_type", "explanation", "file_name", "model",
    "programming_language", "class_name", "method_name",
    "analyse_type", "code", "prompt_type", "prompt",
    "is_composite_prompt", "code_metric"
]

# Variável pai usada como prefixo
name = "qwen2_5_coder_1_5b"
model = "qwen2.5-coder:1.5b"
# Configurações
consultas = [
    {
        "model": f"{model}",
        "analyse_type": "long-parameter-list",
        "prompt_type": "zero-shot",
        "is_composite_prompt": 0,
        "output_csv": f"{name}_long_parameter_list_zero_shot_without_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-parameter-list",
        "prompt_type": "zero-shot",
        "is_composite_prompt": 1,
        "output_csv": f"{name}_long_parameter_list_zero_shot_with_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-parameter-list",
        "prompt_type": "zero-shot-chain-of-thought",
        "is_composite_prompt": 0,
        "output_csv": f"{name}_long_parameter_list_zero_shot_cot_without_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-parameter-list",
        "prompt_type": "zero-shot-chain-of-thought",
        "is_composite_prompt": 1,
        "output_csv": f"{name}_long_parameter_list_zero_shot_cot_with_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-method",
        "prompt_type": "zero-shot",
        "is_composite_prompt": 0,
        "output_csv": f"{name}_long_method_zero_shot_without_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-method",
        "prompt_type": "zero-shot",
        "is_composite_prompt": 1,
        "output_csv": f"{name}_long_method_zero_shot_with_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-method",
        "prompt_type": "zero-shot-chain-of-thought",
        "is_composite_prompt": 0,
        "output_csv": f"{name}_long_method_zero_shot_cot_without_ast.csv"
    },
    {
        "model": f"{model}",
        "analyse_type": "long-method",
        "prompt_type": "zero-shot-chain-of-thought",
        "is_composite_prompt": 1,
        "output_csv": f"{name}_long_method_zero_shot_cot_with_ast.csv"
    },
]

# Executa consultas e gera CSVs
for cfg in consultas:
    query = '''
    SELECT * FROM code_smells_v1
    WHERE model = ?
      AND analyse_type = ?
      AND prompt_type = ?
      AND is_composite_prompt = ?;
    '''
    params = (
        cfg["model"],
        cfg["analyse_type"],
        cfg["prompt_type"],
        cfg["is_composite_prompt"]
    )

    cursor.execute(query, params)
    rows = cursor.fetchall()

    if rows:
        with open(cfg["output_csv"], mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(colunas_code_smells + ["project", "dpy", "pysmell"])  # cabeçalho
            writer.writerows(rows)
        print(f"✅ CSV gerado: {cfg['output_csv']} ({len(rows)} linhas)")
    else:
        print(f"⚠️ Nenhum dado encontrado para: {cfg['output_csv']}")

conn.close()