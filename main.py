import streamlit as st
import pandas as pd

# URL da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789"
oleo_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"

# Lendo as planilhas
data = pd.read_csv(sheet_url, skiprows=1, nrows=11)
oleos = pd.read_csv(oleo_url, header=None, names=["KARDEX", "OLEO"])

# Convertendo colunas numéricas
data["Total"] = pd.to_numeric(data["Total"], errors="coerce", downcast="float")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"].astype(str).str.replace(",", "."), errors="coerce")

# Calculando a diferença
data["Diferença"] = data["Total"] - data["SISTEMA"]

# Mesclando com a descrição do óleo
resultado = pd.merge(data, oleos, left_on="KARDEX", right_on="KARDEX", how="left")

# Selecionando as colunas para exibir
tabela_final = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibindo no app
st.title("Resumo do Estoque Atual:")
st.dataframe(tabela_final)
