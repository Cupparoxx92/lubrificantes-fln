import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório - Última Atualização por Lubrificante", layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# URL do CSV publicado
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Leitura do CSV completo
data = pd.read_csv(csv_url)

# Converte a coluna de data
data["Data"] = pd.to_datetime(data["DATA"], dayfirst=True, errors="coerce")

# Para cada Kardex, pega o registro mais recente
ultimos_registros = data.sort_values("Data").groupby("KARDEX").last().reset_index()

# Monta a tabela final
relatorio = pd.DataFrame({
    "Data": ultimos_registros["Data"],
    "Kardex": ultimos_registros["KARDEX"],
    "Lubrificante": ultimos_registros["LUBRIFICANTE"],
    "Total": pd.to_numeric(ultimos_registros["Total"], errors="coerce"),
    "Sistema": pd.to_numeric(ultimos_registros["Sistema"], errors="coerce"),
})

# Calcula a diferença (Sistema - Total)
relatorio["Diferença"] = relatorio["Sistema"] - relatorio["Total"]

# Mostra o DataFrame no app
st.dataframe(relatorio)
