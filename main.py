import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório Estoque", layout="wide")
st.title("📊 Relatório - Última Atualização por Lubrificante")

# Link do Google Sheets (exportando CSV da aba correta)
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=0"

# Lê a planilha a partir da linha 903, selecionando apenas as colunas A, B, E, F, G (índices 0, 1, 4, 5, 6)
df = pd.read_csv(sheet_url, skiprows=902, usecols=[0, 1, 4, 5, 6], header=None)
df.columns = ["Data", "Kardex", "Total", "Sistema", "Lubrificante"]

# Converte tipos
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
df["Sistema"] = pd.to_numeric(df["Sistema"], errors="coerce").fillna(0)

# Remove registros sem Kardex ou Data
df = df.dropna(subset=["Kardex", "Data"])

# Pega a última data por Kardex
ultimos = df.sort_values("Data").groupby("Kardex", as_index=False).last()

# Calcula a diferença (Sistema - Total)
ultimos["Diferença"] = ultimos["Sistema"] - ultimos["Total"]

# Exibe o resultado
resultado = ultimos[["Data", "Kardex", "Lubrificante", "Total", "Sistema", "Diferença"]]
st.dataframe(resultado, use_container_width=True)
