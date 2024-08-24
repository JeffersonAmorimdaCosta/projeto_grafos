"""
Módulo principal.
"""

from pathlib import Path
import pandas as pd

PASTA_RAIZ = Path(__file__).parent
CAMINHO_CONTRATOS = PASTA_RAIZ / 'data' / 'contratos.csv'

df = pd.read_csv(CAMINHO_CONTRATOS, sep=';').dropna(axis=1, how='all')

df.drop(columns=['NÚMERO DO CONTRATO', 'SITUAÇÃO',
                 'GRUPO DE OBJETO DE CONTRATAÇÃO',
                 'DATA PUBLICAÇÃO DOU', 'DATA ASSINATURA CONTRATO',
                 'ORGÃO SUPERIOR CONTRATANTE',
                 'ÓRGÃO / ENTIDADE VINCULADA CONTRATANTE'], inplace=True)
