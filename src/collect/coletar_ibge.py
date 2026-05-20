import os
import requests
import pandas as pd
from datetime import datetime

URL_ESTADOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

def coletar_estados():
    print("Coletando estados do IBGE...")
    response = requests.get(URL_ESTADOS)
    
    if response.status_code == 200:
        dados = response.json()
        df = pd.DataFrame(dados)[["id", "sigla", "nome"]]
        df = df.sort_values("sigla").reset_index(drop=True)
        print(f"✅ {len(df)} estados coletados com sucesso!")
        return df
    else:
        print(f"❌ Erro na requisição: {response.status_code}")
        return None

def salvar_dados(df, nome_arquivo):
    os.makedirs("data/raw", exist_ok=True)  # cria a pasta se não existir
    timestamp = datetime.now().strftime("%Y%m%d")
    caminho = f"data/raw/{nome_arquivo}_{timestamp}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"💾 Dados salvos em: {caminho}")

if __name__ == "__main__":
    df_estados = coletar_estados()
    if df_estados is not None:
        print(df_estados)
        salvar_dados(df_estados, "estados")