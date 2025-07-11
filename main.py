import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório Estoque", layout="wide")
st.title("📊 Relatório - Última Atualização por Lubrificante")

# Leitura completa da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=0"
df = pd.read_csv(sheet_url)

# Exibe as colunas encontradas
st.write("Colunas encontradas:", list(df.columns))

# Renomeia as colunas (conforme a ordem da planilha)
df.columns = ["Data", "Kardex", "Medida", "Galão", "Total", "Sistema", "Lubrificante"]

# Converte tipos
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
df["Sistema"] = pd.to_numeric(df["Sistema"], errors="coerce").fillna(0)

# Mantém apenas linhas válidas
df = df.dropna(subset=["Kardex", "Data"])

# Busca a última data de cada Kardex
ultimos = df.sort_values("Data").groupby("Kardex", as_index=False).last()

# Calcula a diferença
ultimos["Diferença"] = ultimos["Sistema"] - ultimos["Total"]

# Reordena e exibe
resultado = ultimos[["Data", "Kardex", "Lubrificante", "Total", "Sistema", "Diferença"]]
st.dataframe(resultado, use_container_width=True)
