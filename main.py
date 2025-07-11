import streamlit as st
import pandas as pd

# URL da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789"
oleo_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"

# Leitura da planilha principal
data = pd.read_csv(sheet_url, skiprows=1, nrows=11)

# Mostra os nomes das colunas para conferirmos
st.write("Colunas da planilha:", list(data.columns))

# Renomeia as colunas removendo espaços
data.columns = data.columns.str.strip()

# Conversão dos campos numéricos
data["Total"] = pd.to_numeric(data["Total"], errors="coerce", downcast="float")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"].astype(str).str.replace(",", "."), errors="coerce")

# Calcula a diferença
data["Diferença"] = data["Total"] - data["SISTEMA"]

# Leitura da planilha de óleos
oleos = pd.read_csv(oleo_url, header=None, names=["KARDEX", "OLEO"])

# Faz o merge pelo código do Kardex
resultado = pd.merge(data, oleos, on="KARDEX", how="left")

# Seleciona as colunas desejadas
tabela_final = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibe no app
st.title("Resumo do Estoque Atual:")
st.dataframe(tabela_final)
