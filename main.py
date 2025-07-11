import streamlit as st
import pandas as pd

# URL da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789"
oleo_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"

# Lê a planilha principal
colunas = ["DATA", "KARDEX", "Medida", "Galão", "Total", "SISTEMA"]
data = pd.read_csv(sheet_url, header=None, names=colunas, skiprows=1, nrows=11)

# Converte Total e SISTEMA
data["Total"] = pd.to_numeric(data["Total"], errors="coerce", downcast="float")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"].astype(str).str.replace(",", "."), errors="coerce")

# Calcula a diferença
data["Diferença"] = data["Total"] - data["SISTEMA"]

# Lê os nomes dos óleos
oleos = pd.read_csv(oleo_url, header=None, names=["KARDEX", "OLEO"])

# Faz o merge
resultado = pd.merge(data, oleos, on="KARDEX", how="left")

# Seleciona as colunas finais
tabela_final = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibe no app
st.title("Resumo de Estoque Atual")
st.dataframe(tabela_final)
