import pandas as pd
import os
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)


def gerar_matriz_metricas(y_true, y_pred):
    classes = sorted(list(set(y_true + y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=classes)

    resultados = []
    for idx, classe in enumerate(classes):
        TP = cm[idx, idx]
        FP = cm[:, idx].sum() - TP
        FN = cm[idx, :].sum() - TP

        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        resultados.append({
            'PySmell': classe,
            'LLM': classe,
            'TP': TP,
            'FP': FP,
            'FN': FN,
            'precision': round(precision, 2),
            'recall': round(recall, 2),
            'f1': round(f1, 2)
        })

    return pd.DataFrame(resultados)


def processar_csv(path_csv, output_dir):
    df = pd.read_csv(path_csv)

    # Filtragem e limpeza dos dados
    df = df[df["pysmell"].notnull()]  # remove NaN
    df["pysmell"] = df["pysmell"].astype(int)

    df["smell_type"] = df["smell_type"].map({
        "long parameter list": 1,
        "non-long parameter list": 0,
        # "long method": 1,
        # "non-long method": 0
    }).fillna(-1).astype(int)

    df = df[df["smell_type"] != -1]

    y_true = df["pysmell"].tolist()
    y_pred = df["smell_type"].tolist()

    if not y_true or not y_pred:
        print(f"Aviso: Arquivo {path_csv} não possui dados válidos após filtragem. Pulando.")
        return

    # Geração da matriz de métricas
    df_metricas = gerar_matriz_metricas(y_true, y_pred)

    acc = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(y_true, y_pred, average='macro')
    recall_macro = recall_score(y_true, y_pred, average='macro')
    f1_macro = f1_score(y_true, y_pred, average='macro')

    precision_weighted = precision_score(y_true, y_pred, average='weighted')
    recall_weighted = recall_score(y_true, y_pred, average='weighted')
    f1_weighted = f1_score(y_true, y_pred, average='weighted')

    relatorio = classification_report(
        y_true, y_pred,
        #target_names=["non-long method", "long method"]
        target_names=["non-long parameter list", "long parameter list"]
    )

    # Nome do arquivo de saída
    nome_base = os.path.splitext(os.path.basename(path_csv))[0]
    path_saida = os.path.join(output_dir, f'{nome_base}_metricas.txt')

    with open(path_saida, 'w') as f:
        f.write("=== MÉTRICAS POR CLASSE ===\n")
        f.write(df_metricas.to_string(index=False))
        f.write("\n\n=== MÉTRICAS GERAIS DO MODELO ===\n")
        f.write(f"Acurácia:               {acc:.2f}\n")
        f.write(f"Precision (macro):      {precision_macro:.2f}\n")
        f.write(f"Recall (macro):         {recall_macro:.2f}\n")
        f.write(f"F1 Score (macro):       {f1_macro:.2f}\n")
        f.write(f"Precision (weighted):   {precision_weighted:.2f}\n")
        f.write(f"Recall (weighted):      {recall_weighted:.2f}\n")
        f.write(f"F1 Score (weighted):    {f1_weighted:.2f}\n")
        f.write("\n=== RELATÓRIO COMPLETO ===\n")
        f.write(relatorio)

    print(f"Arquivo salvo: {path_saida}")


def processar_pasta_csvs(pasta_csvs, pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)
    arquivos_csv = [f for f in os.listdir(pasta_csvs) if f.endswith('.csv')]

    for nome_arquivo in arquivos_csv:
        caminho_completo = os.path.join(pasta_csvs, nome_arquivo)
        processar_csv(caminho_completo, pasta_saida)


# === USO ===
name = 'codellama_7b'
pasta_dos_csvs = f'./data/{name}/csvs'
pasta_de_saida = f'./data/{name}'

processar_pasta_csvs(pasta_dos_csvs, pasta_de_saida)
