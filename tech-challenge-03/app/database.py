import os
import pandas as pd
from sqlalchemy import create_engine
import urllib

def inserir_dados_sql():
    path_refined = 'stored-data\\refined_data_excel\\'
    arquivos = os.listdir(path_refined)

    df_completo = pd.DataFrame()

    for arquivo in arquivos:
        caminho = os.path.join(path_refined, arquivo)
        try:
            df = pd.read_excel(caminho)
            df_completo = pd.concat([df_completo, df], ignore_index=True)
        except Exception as e:
            print(f"Erro ao ler {arquivo}: {e}")

    print(f"{len(df_completo)} linhas serão inseridas no banco.")

    connection_string = (
        r"DRIVER={ODBC Driver 17 for SQL Server};"
        r"SERVER=beautyball\SQLEXPRESS;"
        r"DATABASE=mlet-desafio;"
        r"Trusted_Connection=yes;"
    )

    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    df_completo.to_sql('PRECOS_COMBUSTIVEL', con=engine, if_exists='replace', index=False)
    print("Dados inseridos com sucesso no banco de dados.")
