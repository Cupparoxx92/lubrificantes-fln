import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Estoque Lubrificantes", layout="wide")
st.title("📊 Situação do Estoque por Lubrificante")

# URL base da planilha
sheet_id = "1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI"
gid = "879658789"

# Leitura do intervalo A1:G12
url_dados = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}&range=A1:G12"
df_dados = pd.read_csv(url_dados)

# Leitura do intervalo J2:K12 (KARDEX e Nome do Lubrificante)
url_nomes = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}&range=J2:K12"
df_nomes = pd.read_csv(url_nomes, header=None, names=["KARDEX", "Óleo"])

# Junta as duas tabelas usando a coluna KARDEX
df = pd.merge(df_dados, df_nomes, on="KARDEX", how="left")

# Calcula a diferença
df["Diferença"] = df["Total"] - df["SISTEMA"]

# Define a situação
df["Situação"] = df["Diferença"].apply(lambda x: "✅ Sobrando" if x > 0 else ("🔴 Faltando" if x < 0 else "✔️ Certo"))

# Exibe a tabela final
st.subheader("📋 Resumo por Lubrificante")
st.dataframe(df[["KARDEX", "Óleo", "Total", "SISTEMA", "Diferença", "Situação"]])

# Exibe resumo em texto
st.subheader("🔍 Detalhes")
for _, row in df.iterrows():
    st.write(f"KARDEX **{row['KARDEX']}**, **{row['Óleo']}** → {row['Situação']} (Diferença: {round(row['Diferença'], 2)})")
