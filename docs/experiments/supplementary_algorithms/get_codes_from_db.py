# Algoritmo sugerido 

import sqlite3
import os

conn = sqlite3.connect('code_smells.db')
cursor = conn.cursor()

tabela = 'code_smells_v1'
coluna = 'code'

output_dir = 'saida_arquivos'
os.makedirs(output_dir, exist_ok=True)

query = f"SELECT {coluna} FROM {tabela}"
cursor.execute(query)

resultados = cursor.fetchall()

for idx, linha in enumerate(resultados, start=1):
    conteudo = linha[0]
    nome_arquivo = os.path.join(output_dir, f'output_{idx}.py')
    
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

print(f"{len(resultados)} arquivos .py foram gerados na pasta '{output_dir}'.")

cursor.close()
conn.close()