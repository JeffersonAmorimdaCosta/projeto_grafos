"""
Módulo principal.
"""

from utils import formata_numero
from pathlib import Path
import pandas as pd
import networkx as nx

PASTA_RAIZ = Path(__file__).parent
BASE_DE_DADOS = 'contratos.csv'
CAMINHO_CONTRATOS = PASTA_RAIZ / 'data' / BASE_DE_DADOS

df = pd.read_csv(CAMINHO_CONTRATOS, sep=';').dropna(axis=1, how='all')

df.drop(columns=['NÚMERO DO CONTRATO', 'SITUAÇÃO',
                 'GRUPO DE OBJETO DE CONTRATAÇÃO',
                 'DATA PUBLICAÇÃO DOU', 'DATA ASSINATURA CONTRATO',
                 'ÓRGÃO / ENTIDADE VINCULADA CONTRATANTE',
                 'FORMA DE CONTRATAÇÃO'], inplace=True)

G = nx.Graph()

for indice, linha in df.iterrows():
    orgao_contratante: str = linha['ORGÃO SUPERIOR CONTRATANTE']
    nome_empresa: str = linha['NOME DO FORNECEDOR']
    cnpj_cpf_empresa: str = linha['CPF / CNPJ DO FORNECEDOR']
    valor_contrato_str: str = linha['VALOR CONTRATADO']

    valor_contrato_str = formata_numero(valor_contrato_str)

    try:
        valor_contrato = float(valor_contrato_str)
    except ValueError:
        continue

    if valor_contrato < 0:
        continue

    if nome_empresa not in G:
        G.add_node(nome_empresa, dado=cnpj_cpf_empresa)

    G.add_edge(orgao_contratante, nome_empresa, weight=valor_contrato)

nx.write_gexf(G, "grafo.gexf")
