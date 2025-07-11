import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Estoque Lubrificantes", layout="wide")
st.title("Resumo do Estoque Atual:")

# URLs e intervalos da planilha
sheet_id = "1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI"
gid = "879658789"
data_range = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}&range=A1:G12"
nomes_range = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}&range=J2:K12"

# Leitura dos dados
df = pd.read_csv(data_range, header=0)
nomes = pd.read_csv(nomes_range, header=None, names=["KARDEX", "OLEO"])

# Conversão das colunas numéricas (corrige erros caso tenha texto ou vazios)
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
df["SISTEMA"] = pd.to_numeric(df["SISTEMA"], errors="coerce").fillna(0)

# Cálculo da diferença
df["Diferença"] = df["Total"] - df["SISTEMA"]

# Junção com o nome dos óleos
resultado = pd.merge(df, nomes, on="KARDEX", how="left")

# Reordena as colunas para exibir melhor
resultado = resultado[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibição no app
st.dataframe(resultado)
