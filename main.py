import pandas as pd
import streamlit as st
from io import StringIO
import requests

# URL da planilha publicada como CSV
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"
data = pd.read_csv(sheet_url)

data['DATA'] = pd.to_datetime(data['DATA'], errors='coerce', dayfirst=True)
data['TOTAL'] = pd.to_numeric(data['TOTAL'], errors='coerce')
data['SISTEMA'] = pd.to_numeric(data['SISTEMA'], errors='coerce')

# Obter a última data de cada lubrificante
ultimos_registros = data.sort_values('DATA').groupby('LUBRIFICANTE', as_index=False).last()
ultimos_registros['DIFERENCA'] = ultimos_registros['SISTEMA'] - ultimos_registros['TOTAL']

# Layout do dashboard
st.set_page_config(page_title="Relatório - Última Atualização por Lubrificante", layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# Tabela principal
st.dataframe(
    ultimos_registros[['DATA', 'KARDEX', 'LUBRIFICANTE', 'TOTAL', 'SISTEMA', 'DIFERENCA']]
    .style.format({'TOTAL': '{:.0f}', 'SISTEMA': '{:.0f}', 'DIFERENCA': '{:+.0f}'})
    .apply(lambda x: [
        "color: green" if v > 0 else "color: red" if v < 0 else "" for v in x
    ] if x.name == 'DIFERENCA' else ["" for _ in x], axis=0),
    hide_index=True,
    use_container_width=True
)

# Cards individuais
st.subheader("Resumo por Lubrificante")
for _, row in ultimos_registros.iterrows():
    sobra_falta = row['DIFERENCA']
    acuracidade = (min(row['TOTAL'], row['SISTEMA']) / max(row['TOTAL'], row['SISTEMA'])) * 100 if max(row['TOTAL'], row['SISTEMA']) > 0 else 100

    with st.container():
        st.markdown(f"### {row['KARDEX']} - {row['LUBRIFICANTE']}")
        col1, col2 = st.columns([3, 3])
        with col1:
            st.metric("Físico", f"{int(row['TOTAL'])}" if pd.notnull(row['TOTAL']) else "-")
            st.metric("Sistema", f"{int(row['SISTEMA'])}" if pd.notnull(row['SISTEMA']) else "-")
        with col2:
            st.metric("Diferença (L)", f"{sobra_falta:+.0f}", delta_color="inverse" if sobra_falta < 0 else "normal")
            st.metric("% Acuracidade", f"{acuracidade:.1f}%")
