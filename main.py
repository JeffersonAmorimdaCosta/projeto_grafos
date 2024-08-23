import pandas as pd
import csv

# Especificar o caminho do arquivo CSV
csv_file_path = 'contrato.csv'

try:
    # Tentar ler o CSV especificando o delimitador e ignorando linhas problemáticas
    df = pd.read_csv(
        csv_file_path,
        delimiter=';',         # Tente especificar o delimitador correto
        encoding='utf-8',      # Especifique a codificação
        on_bad_lines='skip',   # Ignore linhas com problemas
        quoting=csv.QUOTE_NONE # Se necessário, desative o comportamento de aspas
    )

    # Exibir as primeiras linhas do DataFrame
    print("Primeiras linhas do DataFrame:")
    print(df.head())

    # Ler o arquivo em chunks para identificar possíveis problemas em blocos menores
    chunksize = 1000
    print("\nLeitura em chunks para verificar partes do arquivo:")
    for chunk in pd.read_csv(
        csv_file_path,
        delimiter=';',
        encoding='utf-8',
        chunksize=chunksize,
        on_bad_lines='skip',
        quoting=csv.QUOTE_NONE
    ):
        print(chunk.head())

except pd.errors.ParserError as e:
    # Identificar a linha problemática caso ocorra um erro
    print("Erro ao ler o arquivo CSV:")
    print(e)


except Exception as e:

    print("Ocorreu um erro inesperado:")
    print(e)

finally:
    print("\nProcessamento do arquivo CSV finalizado.")

