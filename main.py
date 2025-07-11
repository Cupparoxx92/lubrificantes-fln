import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Leitura da planilha CSV publicada
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv'
data = pd.read_csv(url)

# Convertendo datas e filtrando últimas leituras por Kardex
data['DATA'] = pd.to_datetime(data['DATA'], dayfirst=True, errors='coerce')
ultimos_registros = data.sort_values('DATA').groupby('KARDEX').last().reset_index()

# Corrigindo casas decimais e calculando diferença e acuracidade
ultimos_registros['TOTAL'] = pd.to_numeric(ultimos_registros['TOTAL'], errors='coerce').fillna(0).astype(int)
ultimos_registros['SISTEMA'] = pd.to_numeric(ultimos_registros['SISTEMA'], errors='coerce').fillna(0).astype(int)
ultimos_registros['DIFERENCA'] = ultimos_registros['TOTAL'] - ultimos_registros['SISTEMA']
ultimos_registros['% Acuracidade'] = (ultimos_registros['TOTAL'] / ultimos_registros['SISTEMA'].replace(0, pd.NA)) * 100
ultimos_registros['% Acuracidade'] = ultimos_registros['% Acuracidade'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "-")

# ---------- Layout ----------
st.set_page_config(layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# ---------- Tabela Principal ----------
tabela_cols = ['DATA', 'KARDEX', 'LUBRIFICANTE', 'TOTAL', 'SISTEMA', 'DIFERENCA']
tabela_formatada = ultimos_registros.copy()
tabela_formatada['DATA'] = tabela_formatada['DATA'].dt.strftime('%Y-%m-%d')
tabela_formatada['DIFERENCA'] = tabela_formatada['DIFERENCA'].apply(
    lambda x: f"+{x}" if x > 0 else (f"{x}" if x < 0 else "+0")
)

# Colorindo diferença
def cor_diferenca(val):
    if '+' in val:
        return f"<span style='color:green'>{val}</span>"
    elif '-' in val:
        return f"<span style='color:red'>{val}</span>"
    return val

tabela_formatada['DIFERENCA'] = tabela_formatada['DIFERENCA'].apply(cor_diferenca)

# Renderizando tabela
st.markdown(
    tabela_formatada[tabela_cols].to_html(escape=False, index=False),
    unsafe_allow_html=True
)

# ---------- Barras Laterais por Lubrificante ----------
st.markdown("## Diferença por Óleo")

cols = st.columns(2)
for idx, row in enumerate(ultimos_registros.itertuples()):
    col = cols[idx % 2]
    with col:
        st.markdown(f"**{row.KARDEX} - {row.LUBRIFICANTE}**")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[''],
            x=[row.TOTAL],
            name='Físico',
            orientation='h',
            marker_color='royalblue',
            text=[row.TOTAL],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            y=[''],
            x=[row.SISTEMA],
            name='Sistema',
            orientation='h',
            marker_color='orangered',
            text=[row.SISTEMA],
            textposition='outside'
        ))

        fig.update_layout(
            barmode='group',
            height=150,
            margin=dict(l=20, r=20, t=10, b=20),
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
        )

        st.plotly_chart(fig, use_container_width=True)

        diferenca = row.DIFERENCA
        seta = '⬆' if diferenca > 0 else ('⬇' if diferenca < 0 else '➡')
        cor = 'green' if diferenca > 0 else ('red' if diferenca < 0 else 'gray')
        st.markdown(f"<span style='font-size:20px; color:{cor};'>{seta} {abs(diferenca)} L</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-size:16px;'>% Acuracidade: <strong>{row._8}</strong></span>", unsafe_allow_html=True)
