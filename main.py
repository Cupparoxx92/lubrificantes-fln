import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Situação do Estoque por Lubrificante", layout="wide")
st.title("Situação do Estoque por Lubrificante")

# Base do link
sheet_base = "https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/export?format=csv&gid=879658789"

# Leitura dos lubrificantes (J2:K12)
oleo_url = sheet_base + "&range=J2:K12"
oleo_df = pd.read_csv(oleo_url, header=None, names=["KARDEX", "OLEO"])

# Leitura do Total (E2:E12)
total_url = sheet_base + "&range=E2:E12"
total_df = pd.read_csv(total_url, header=None, names=["Total"])

# Leitura do Sistema (F2:F12)
sistema_url = sheet_base + "&range=F2:F12"
sistema_df = pd.read_csv(sistema_url, header=None, names=["Sistema"])

# Junta as informações
dados = pd.concat([oleo_df, total_df, sistema_df], axis=1)

# Conversão numérica
dados["Total"] = pd.to_numeric(dados["Total"], errors="coerce")
dados["Sistema"] = pd.to_numeric(dados["Sistema"], errors="coerce")

# Calcula diferença
dados["Diferença"] = dados["Total"] - dados["Sistema"]

# Exibe o resultado
st.dataframe(dados)
