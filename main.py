import streamlit as st
import pandas as pd

# Configuração do app
st.set_page_config(page_title="Relatório - Última Atualização por Lubrificante", layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# URL da planilha (público como CSV)
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Leitura da planilha
data = pd.read_csv(csv_url)

# Converte a coluna "DATA" para datetime
data["DATA"] = pd.to_datetime(data["DATA"], dayfirst=True, errors="coerce")

# Garante que TOTAL e SISTEMA sejam numéricos (mesmo com fórmula)
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Busca o último registro de cada KARDEX
ultimos_registros = data.sort_values("DATA").groupby("KARDEX").last().reset_index()

# Monta o relatório final
relatorio = ultimos_registros[["DATA", "KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA"]].copy()
relatorio["Diferença"] = relatorio["SISTEMA"] - relatorio["TOTAL"]

# Exibe o relatório
st.dataframe(relatorio)
