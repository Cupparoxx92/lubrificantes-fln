import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import gspread
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials

# Autenticação Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
with open("/mnt/data/02ae0f52-81b3-4cf9-850c-ac5b0c480dc7.json") as source:
    credentials = Credentials.from_service_account_file(source.name, scopes=scope)
client = gspread.authorize(credentials)

# Leitura dos dados da planilha
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/edit")
sheet = spreadsheet.get_worksheet(0)
data = get_as_dataframe(sheet, evaluate_formulas=True)
data = data.dropna(subset=["KARDEX"])  # Somente linhas válidas

# Conversão de colunas numéricas (garante leitura correta mesmo com fórmulas)
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Última leitura por Kardex
ultimos = data.sort_values("DATA").groupby("KARDEX").tail(1).sort_values("KARDEX")

# Cálculo da diferença e conversão para int (substitui NaN por 0)
ultimos["DIFERENCA"] = (ultimos["TOTAL"] - ultimos["SISTEMA"]).fillna(0).astype(int)
ultimos["TOTAL"] = ultimos["TOTAL"].fillna(0).astype(int)
ultimos["SISTEMA"] = ultimos["SISTEMA"].fillna(0).astype(int)

# Layout principal
st.set_page_config(layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# Exibição da tabela
def color_diferenca(val):
    return "color: green" if val > 0 else ("color: red" if val < 0 else "")

tabela = ultimos[["KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA", "DIFERENCA"]]
st.dataframe(tabela.style.applymap(color_diferenca, subset=["DIFERENCA"]), use_container_width=True)

# Cards laterais com barras horizontais
st.subheader("Diferença por Óleo")

# Quebra a tela horizontalmente
main_col, cards_col = st.columns([3, 2])

with cards_col:
    for _, row in ultimos.iterrows():
        kardex = row["KARDEX"]
        nome = row["LUBRIFICANTE"]
        fisico = row["TOTAL"]
        sistema = row["SISTEMA"]
        diferenca = fisico - sistema

        if fisico + sistema == 0:
            acuracidade = 0
        else:
            acuracidade = round(100 * (1 - abs(diferenca) / max(fisico, sistema)), 1)

        st.markdown(f"#### {kardex} - {nome}")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=["Estoque"],
            x=[fisico],
            orientation="h",
            name="Físico",
            marker_color="blue",
            text=[f"{fisico}"],
            textposition="inside"
        ))
        fig.add_trace(go.Bar(
            y=["Estoque"],
            x=[sistema],
            orientation="h",
            name="Sistema",
            marker_color="orange",
            text=[f"{sistema}"],
            textposition="inside"
        ))
        fig.update_layout(barmode="overlay", height=100, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

        cor = "green" if diferenca > 0 else ("red" if diferenca < 0 else "black")
        seta = "↑" if diferenca > 0 else ("↓" if diferenca < 0 else "")

        st.markdown(f"<span style='color:{cor}'>{seta}{diferenca}L</span>", unsafe_allow_html=True)
        st.write(f"Acuracidade: {acuracidade}%")

# Remove a coluna DATA da tabela e ajusta a leitura para fórmulas
# A tabela principal e os cards ficam exibidos simultaneamente.
