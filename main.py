import streamlit as st
import pandas as pd

# Título do app
st.set_page_config(page_title="Situação do Estoque", layout="wide")
st.title("Situação do Estoque por Lubrificante")

# Leitura da planilha principal
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=A1:G12"
data = pd.read_csv(sheet_url)

# Conversões de tipo
data["Medida"] = pd.to_numeric(data["Medida"], errors="coerce").fillna(0)
data["Galão"] = pd.to_numeric(data["Galão"], errors="coerce").fillna(0)
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce").fillna(0)

# Calcula Total
data["Total"] = data["Medida"] + data["Galão"]

# Leitura dos nomes dos lubrificantes
oleos_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"
oleos = pd.read_csv(oleos_url, header=None, names=["KARDEX", "OLEO"])

# Conversão para string para garantir o merge correto
data["KARDEX"] = data["KARDEX"].astype(str)
oleos["KARDEX"] = oleos["KARDEX"].astype(str)

# Merge entre as tabelas
resultado = pd.merge(data, oleos, on="KARDEX", how="left")

# Cálculo da diferença
resultado["Diferença"] = resultado["Total"] - resultado["SISTEMA"]

# Seleção das colunas finais
tabela_final = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibição da tabela
st.dataframe(tabela_final, use_container_width=True)
