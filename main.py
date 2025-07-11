import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from google.oauth2 import service_account
from gspread_dataframe import get_as_dataframe
import gspread

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(credentials)

# Leitura da planilha e aba
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI/edit")
sheet = spreadsheet.get_worksheet(0)

# Leitura dos dados ignorando as linhas 2 a 902
data = get_as_dataframe(sheet, evaluate_formulas=True)
data = data.dropna(subset=["KARDEX"])  # Filtrar linhas válidas

# Converter colunas numéricas corretamente
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Pegar o último registro de cada óleo
ultimos_registros = data.sort_values("DATA").groupby("KARDEX").tail(1)
ultimos_registros = ultimos_registros.sort_values("KARDEX")

# Calcular a diferença
ultimos_registros["DIFERENCA"] = ultimos_registros["TOTAL"] - ultimos_registros["SISTEMA"]

# Formatar os números como inteiros
ultimos_registros["TOTAL"] = ultimos_registros["TOTAL"].fillna(0).astype(int)
ultimos_registros["SISTEMA"] = ultimos_registros["SISTEMA"].fillna(0).astype(int)
ultimos_registros["DIFERENCA"] = ultimos_registros["DIFERENCA"].fillna(0).astype(int)

# Tabela principal
st.title("Relatório - Última Atualização por Lubrificante")
tabela = ultimos_registros[["KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA", "DIFERENCA"]]

# Estilo de cores nas diferenças
def color_diferenca(val):
    if val > 0:
        return f"color: green"
    elif val < 0:
        return f"color: red"
    else:
        return ""

st.dataframe(
    tabela.style.applymap(color_diferenca, subset=["DIFERENCA"]),
    use_container_width=True
)

# Gráficos laterais
st.subheader("Diferença por Óleo")
cols = st.columns(2)

for i, (_, row) in enumerate(ultimos_registros.iterrows()):
    col = cols[i % 2]

    # Calcular acuracidade
    total = row["TOTAL"]
    sistema = row["SISTEMA"]
    if total + sistema == 0:
        acuracidade = 0
    else:
        acuracidade = round(100 * (1 - abs(total - sistema) / max(total, sistema)), 1)

    with col:
        st.markdown(f"### {row['KARDEX']} - {row['LUBRIFICANTE']}")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[""],
            x=[total],
            orientation='h',
            name='Físico',
            marker_color='blue',
            text=[f"{total}"],
            textposition='inside'
        ))
        fig.add_trace(go.Bar(
            y=[""],
            x=[sistema],
            orientation='h',
            name='Sistema',
            marker_color='orange',
            text=[f"{sistema}"],
            textposition='inside'
        ))
        fig.update_layout(barmode='overlay', height=140, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))

        st.plotly_chart(fig, use_container_width=True)

        diferenca = total - sistema
        st.write(f"Diferença (L): {'+' if diferenca > 0 else ''}{diferenca}")
        st.write(f"% Acuracidade: {acuracidade}%")
