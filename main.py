import streamlit as st
import pandas as pd

# Título da página
st.set_page_config(page_title="Situação do Estoque por Lubrificante", layout="wide")
st.title("Situação do Estoque por Lubrificante")

# Links da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=A1:G12"
lub_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789&range=J2:K12"

# Leitura dos dados
df = pd.read_csv(sheet_url)
nomes = pd.read_csv(lub_url, header=None, names=["KARDEX", "OLEO"])

# Convertendo para numérico com tratamento de erros
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
df["SISTEMA"] = pd.to_numeric(df["SISTEMA"], errors="coerce").fillna(0)

# Calcula a diferença
df["Diferença"] = df["Total"] - df["SISTEMA"]

# Junta o nome do óleo
df = df.merge(nomes, on="KARDEX", how="left")

# Reorganiza as colunas
df = df[["KARDEX", "OLEO", "Total", "SISTEMA", "Diferença"]]

# Exibe os dados
st.subheader("Resumo do Estoque Atual:")
st.dataframe(df)

# Mostra a situação resumida
st.subheader("Situação por Lubrificante:")
for _, row in df.iterrows():
    status = "Faltando" if row["Diferença"] < 0 else "Sobrando"
    st.write(f"🛢️ {row['OLEO']}: {status} {abs(row['Diferença'])}")
