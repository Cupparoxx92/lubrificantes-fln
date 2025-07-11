import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Situação do Estoque por Lubrificante", layout="wide")
st.title("Situação do Estoque por Lubrificante")

# Link da planilha
sheet_url = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv"

# Leitura dos dados principais (A2:F12)
dados_url = sheet_url + "&gid=879658789&range=A2:F12"
dados = pd.read_csv(dados_url)

# Ajuste dos cabeçalhos
dados.columns = ["DATA", "KARDEX_PLAN", "Medida", "Galão", "Total", "Sistema"]

# Leitura dos nomes dos lubrificantes (J2:K12)
oleos_url = sheet_url + "&gid=879658789&range=J2:K12"
oleos = pd.read_csv(oleos_url, header=None, names=["KARDEX", "OLEO"])

# Conversão para numérico
dados["Total"] = pd.to_numeric(dados["Total"], errors="coerce")
dados["Sistema"] = pd.to_numeric(dados["Sistema"], errors="coerce")

# Cálculo da diferença
dados["Diferença"] = dados["Total"] - dados["Sistema"]

# Junta com os nomes dos lubrificantes
resultado = pd.merge(oleos, dados[["KARDEX_PLAN", "Total", "Sistema", "Diferença"]],
                     left_on="KARDEX", right_on="KARDEX_PLAN", how="left")

# Seleção das colunas finais
resultado_final = resultado[["KARDEX", "OLEO", "Total", "Sistema", "Diferença"]]

# Exibição
st.dataframe(resultado_final)
