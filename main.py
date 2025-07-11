import pandas as pd
import streamlit as st
import requests
import io
from datetime import datetime
import plotly.graph_objects as go

# URL CSV Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Lê CSV online
res = requests.get(url)
data = pd.read_csv(io.StringIO(res.content.decode("utf-8")))

data["DATA"] = pd.to_datetime(data["DATA"], dayfirst=True, errors="coerce")
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Pega a última data de cada Kardex
ultimos = data.sort_values("DATA").groupby("KARDEX", as_index=False).last()

# Calcula diferença
ultimos["DIFERENCA"] = ultimos["TOTAL"] - ultimos["SISTEMA"]

# Formata a data
ultimos["DATA"] = ultimos["DATA"].dt.strftime("%d/%m/%Y")

# Mostra a tabela no layout
st.title("Relatório - Última Atualização por Lubrificante")
def format_diff(x):
    if pd.isna(x):
        return "None"
    color = "green" if x > 0 else "red" if x < 0 else "black"
    arrow = "↑" if x > 0 else "↓" if x < 0 else "→"
    return f"<span style='color:{color}'>{arrow} {abs(int(x))}</span>"

tabela = ultimos[["DATA", "KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA", "DIFERENCA"]].copy()
tabela["TOTAL"] = tabela["TOTAL"].fillna("-").apply(lambda x: int(x) if isinstance(x, float) else x)
tabela["SISTEMA"] = tabela["SISTEMA"].fillna("-").apply(lambda x: int(x) if isinstance(x, float) else x)
tabela["DIFERENCA"] = tabela["DIFERENCA"].apply(format_diff)

# Exibe tabela formatada
st.write(tabela.to_html(escape=False, index=False), unsafe_allow_html=True)

# Cards individuais
st.subheader("Acuracidade por Lubrificante")

for _, row in ultimos.iterrows():
    fisico = row["TOTAL"]
    sistema = row["SISTEMA"]

    if pd.isna(fisico) or pd.isna(sistema):
        continue

    diferenca = fisico - sistema
    acuracidade = 100 * min(fisico, sistema) / max(fisico, sistema) if max(fisico, sistema) != 0 else 0

    st.markdown(f"#### {row['KARDEX']} - {row['LUBRIFICANTE']}")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Físico"], y=[fisico], name="Físico", marker_color="blue", text=[int(fisico)], textposition="outside"))
    fig.add_trace(go.Bar(x=["Sistema"], y=[sistema], name="Sistema", marker_color="orange", text=[int(sistema)], textposition="outside"))
    fig.update_layout(barmode="group", height=250, margin=dict(t=20, b=20))

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric("Diferença (L)", f"{int(diferenca):+}", delta_color="inverse")
        st.metric("% Acuracidade", f"{acuracidade:.1f}%")
