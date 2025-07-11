import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Estoque Lubrificantes", layout="wide")
st.title("🔍 Relatório Final por Óleo")

# URL da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=0"

# Lê a planilha inteira e ignora as 902 primeiras linhas
df = pd.read_csv(sheet_url, skiprows=902)

# Nomeia as colunas conforme sua planilha
df.columns = ["Data", "Kardex", "Medida", "Galão", "Total", "Sistema", "Lubrificante"]

# Converte a Data e os números
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
df["Sistema"] = pd.to_numeric(df["Sistema"], errors="coerce").fillna(0)

# Remove linhas sem Kardex ou Data
df = df.dropna(subset=["Kardex", "Data"])

# Busca a última data por Kardex
ultima_data = df.sort_values("Data").groupby("Kardex").tail(1)

# Calcula a diferença (Sistema - Total)
ultima_data["Diferença"] = ultima_data["Sistema"] - ultima_data["Total"]

# Seleciona e exibe as colunas finais
resultado = ultima_data[["Data", "Kardex", "Lubrificante", "Total", "Sistema", "Diferença"]]
st.dataframe(resultado, use_container_width=True)
