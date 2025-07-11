import streamlit as st
import pandas as pd

# Título do app
st.set_page_config(page_title="Situação do Estoque", layout="wide")
st.title("Situação do Estoque por Lubrificante")

# Leitura da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=A1:G12"
data = pd.read_csv(sheet_url)

# Corrige tipos numéricos
data["Medida"] = pd.to_numeric(data["Medida"], errors="coerce")
data["Galão"] = pd.to_numeric(data["Galão"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Calcula corretamente o Total
data["Total"] = data["Medida"] + data["Galão"]

# Lê a tabela de óleos
oleos_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"
oleos = pd.read_csv(oleos_url, header=None, names=["KARDEX", "OLEO"])

# Converte KARDEX para string
data["KARDEX"] = data["KARDEX"].astype(str)
oleos["KARDEX"] = oleos["KARDEX"].astype(str)

# Merge
resultado = pd.merge(data, oleos, on="KARDEX", how="left")

# Calcula a diferença
resultado["Diferença"] = resultado["Total"] - resultado["SISTEMA"]

# Seleção final
tabela_final = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibe no app
st.dataframe(tabela_final, use_container_width=True)
