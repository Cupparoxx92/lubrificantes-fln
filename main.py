import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório Estoque", layout="wide")
st.title("📊 Relatório - Última Atualização por Lubrificante")

# Lê toda a planilha e ignora as primeiras 902 linhas
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=0"
df = pd.read_csv(sheet_url, skiprows=902)

# Exibe os nomes das colunas para validar
st.write("Colunas encontradas:", list(df.columns))

# Renomeia as colunas (ajuste conforme os nomes reais da sua planilha!)
df.columns = ["Data", "Kardex", "Medida", "Galão", "Total", "Sistema", "Lubrificante"]

# Seleciona apenas as colunas necessárias
df = df[["Data", "Kardex", "Total", "Sistema", "Lubrificante"]]

# Converte os tipos
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True, errors="coerce")
df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
df["Sistema"] = pd.to_numeric(df["Sistema"], errors="coerce").fillna(0)

# Filtra linhas válidas
df = df.dropna(subset=["Kardex", "Data"])

# Busca a última data de cada Kardex
ultimos = df.sort_values("Data").groupby("Kardex", as_index=False).last()

# Calcula a diferença
ultimos["Diferença"] = ultimos["Sistema"] - ultimos["Total"]

# Exibe o resultado final
resultado = ultimos[["Data", "Kardex", "Lubrificante", "Total", "Sistema", "Diferença"]]
st.dataframe(resultado, use_container_width=True)
