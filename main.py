import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Exemplo de dados - substitua pelos seus dados reais
data = [
    {'KARDEX': '40300012', 'OLEO': 'OLEO (RETARDER) ATF DEXRON III (TAMBOR 200LTS)', 'TOTAL': 153, 'SISTEMA': 144},
    {'KARDEX': '40300040', 'OLEO': 'ANTI CORROSIVO ORGANICO LARANJA...', 'TOTAL': 1000, 'SISTEMA': 1405},
    {'KARDEX': '40300042', 'OLEO': 'OLEO LUBRIFICANTE MINERAL 15W40 MOTOR EURO 6', 'TOTAL': 713, 'SISTEMA': 716},
]

# Função para criar o gráfico de barras e informações num card
def create_card(kardex, oleo, total, sistema):
    diferenca = total - sistema
    acuracidade = (min(total, sistema) / max(total, sistema)) * 100 if max(total, sistema) != 0 else 100

    # Cores e prefixo da diferença
    if diferenca > 0:
        cor_dif = 'green'
        prefixo = '+'
    elif diferenca < 0:
        cor_dif = 'red'
        prefixo = ''
    else:
        cor_dif = 'gray'
        prefixo = ''

    # Gráfico
    fig = go.Figure(data=[
        go.Bar(name='Físico', y=[''], x=[total], orientation='h', marker_color='royalblue', text=[f'{total}'], textposition='outside'),
        go.Bar(name='Sistema', y=[''], x=[sistema], orientation='h', marker_color='orange', text=[f'{sistema}'], textposition='outside'),
    ])
    fig.update_layout(barmode='group', height=150, margin=dict(l=20, r=20, t=20, b=20), showlegend=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))

    # Card visual
    with st.container():
        st.markdown(f'##### {kardex} - {oleo}')
        st.plotly_chart(fig, use_container_width=True)
        st.write(f'<div style="font-size: 16px;">Diferença (L): <span style="color:{cor_dif};">{prefixo}{diferenca}</span></div>', unsafe_allow_html=True)
        st.write(f'<div style="font-size: 16px;">% Acuracidade: <strong>{acuracidade:.1f}%</strong></div>', unsafe_allow_html=True)

# LAYOUT EM COLUNAS
cols = st.columns(len(data))
for idx, item in enumerate(data):
    with cols[idx]:
        create_card(item['KARDEX'], item['OLEO'], item['TOTAL'], item['SISTEMA'])
