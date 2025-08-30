import sqlite3
import pandas as pd


caminho_csv = 'dados.csv' #Arquivo de extração com os smells que veio do banco
caminho_banco = 'code_smells.db'
tabela_banco = 'long_method' #long_parameter_list


df = pd.read_csv(caminho_csv)


conn = sqlite3.connect(caminho_banco)
cursor = conn.cursor()


for index, row in df.iterrows():
    file_name_csv = row['file_name']
    
 
    query = f"""
    SELECT project, dpy, pysmell 
    FROM {tabela_banco}
    WHERE file_name = ?
    """
    cursor.execute(query, (file_name_csv,))
    resultado = cursor.fetchone()
    
    if resultado:
        df.at[index, 'project'] = resultado[0]
        df.at[index, 'dpy'] = resultado[1]
        df.at[index, 'pysmell'] = resultado[2]


cursor.close()
conn.close()


df.to_csv('dados_atualizado.csv', index=False)

print("CSV atualizado e salvo como 'dados_atualizado.csv'.")
