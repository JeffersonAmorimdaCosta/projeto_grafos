"""
Módulo principal.
"""

from pathlib import Path
import pandas as pd
import networkx as nx
from utils import formata_numero

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

# nx.write_gexf(G, "grafo.gexf")

empresas = df['NOME DO FORNECEDOR'].unique()

centralidade = nx.degree_centrality(G)
intermediacao = nx.betweenness_centrality(G)

centralidade_empresas = {e: centralidade[e]
                         for e in empresas if e in centralidade}

intermediacao_empresas = {e: intermediacao[e]
                          for e in empresas if e in intermediacao}

print("quantidade de empresas: ", len(empresas))

media_centralidade = sum(centralidade_empresas.values()
                         ) / len(centralidade_empresas)

media_intermediacao = sum(intermediacao_empresas.values()
                          ) / len(intermediacao_empresas)

acima_media_centralidade = {e: p for e, p in centralidade_empresas.items()
                            if p > media_centralidade}

acima_media_intermediacao = {e: p for e, p in intermediacao_empresas.items()
                             if p > media_intermediacao}

print('quantidade empresas acima da media em centralidade: ',
      len(acima_media_centralidade))

print('quantidade empresas acima da media em intermediacao: ',
      len(acima_media_intermediacao))

empresas_resultantes_acima = set(acima_media_centralidade.keys()) & set(
    acima_media_intermediacao.keys())

print('Quantidade empresas na intersecção: ',
      len((empresas_resultantes_acima)))

for e in empresas_resultantes_acima:
    print(e)
