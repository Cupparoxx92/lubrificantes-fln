import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório - Última Atualização por Lubrificante", layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# URL da planilha publicada em CSV
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Leitura e tratamento dos dados
data = pd.read_csv(csv_url)
data.columns = data.columns.str.strip().str.upper()

# Converter campos numéricos
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Buscar o último registro por Kardex
ultimos = data.sort_values("DATA").groupby("KARDEX").last().reset_index()

# Calcular diferença
ultimos["DIFERENÇA"] = ultimos["SISTEMA"] - ultimos["TOTAL"]

# Formatar a diferença com setas
def formatar_diferenca(valor):
    if pd.isna(valor):
        return "—"
    if valor > 0:
        return f"🟢 ↑ {valor:.0f}"
    elif valor < 0:
        return f"🔴 ↓ {abs(valor):.0f}"
    else:
        return "0"

ultimos["DIFERENÇA"] = ultimos["DIFERENÇA"].apply(formatar_diferenca)

# Selecionar e renomear as colunas
resultado = ultimos[["DATA", "KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA", "DIFERENÇA"]]

# Mostrar tabela sem o índice lateral
st.dataframe(resultado.reset_index(drop=True), use_container_width=True)
