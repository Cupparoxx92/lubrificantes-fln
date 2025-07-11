import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório - Última Atualização por Lubrificante", layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# URL do CSV (publicado corretamente)
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Leitura do CSV e correção de cabeçalhos
data = pd.read_csv(csv_url, sep=",", encoding="utf-8", skiprows=0)
data.columns = data.columns.str.strip().str.upper()

# Verificar colunas
esperadas = ['DATA', 'KARDEX', 'MEDIDA', 'GALAO', 'TOTAL', 'SISTEMA', 'LUBRIFICANTE']
faltando = [col for col in esperadas if col not in data.columns]
if faltando:
    st.error(f"Colunas faltando no CSV: {faltando}")
    st.stop()

# Converter TOTAL e SISTEMA para numérico (caso sejam fórmulas)
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Obter a última data para cada Kardex
ultimos_registros = data.sort_values("DATA").groupby("KARDEX").last().reset_index()

# Calcular a diferença
ultimos_registros["DIFERENÇA"] = ultimos_registros["SISTEMA"] - ultimos_registros["TOTAL"]

# Selecionar e renomear colunas
resultado = ultimos_registros[["DATA", "KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA", "DIFERENÇA"]]

# Exibir tabela
st.dataframe(resultado, use_container_width=True)
