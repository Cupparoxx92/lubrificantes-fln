import streamlit as st
import pandas as pd

# Título do app
st.set_page_config(page_title="Situação do Estoque", layout="wide")
st.title("Situação do Estoque por Lubrificante")

# Link da planilha e leitura
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=A1:G12"
data = pd.read_csv(sheet_url)

# Converte colunas numéricas (caso estejam como texto)
data["Total"] = pd.to_numeric(data["Total"], errors="coerce", downcast="float")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce", downcast="float")

# Lê os nomes dos óleos (faixa J2:K12)
oleos_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"
oleos = pd.read_csv(oleos_url, header=None, names=["KARDEX", "OLEO"])

# Converte a coluna KARDEX para string para evitar erro no merge
data["KARDEX"] = data["KARDEX"].astype(str)
oleos["KARDEX"] = oleos["KARDEX"].astype(str)

# Merge
resultado = pd.merge(data, oleos, on="KARDEX", how="left")

# Calcula a diferença entre Total e SISTEMA
resultado["Diferença"] = resultado["Total"] - resultado["SISTEMA"]

# Seleciona as colunas finais que você quer mostrar
tabela_final = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibe no app
st.dataframe(tabela_final, use_container_width=True)
