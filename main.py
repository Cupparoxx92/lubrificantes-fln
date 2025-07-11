import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Relatório - Última Atualização por Lubrificante", layout="wide")
st.title("Relatório - Última Atualização por Lubrificante")

# URL da planilha publicada em CSV
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Leitura da planilha
data = pd.read_csv(csv_url)
data.columns = data.columns.str.strip().str.upper()

# Converter colunas numéricas
data["TOTAL"] = pd.to_numeric(data["TOTAL"], errors="coerce")
data["SISTEMA"] = pd.to_numeric(data["SISTEMA"], errors="coerce")

# Corrige a coluna de data
data["DATA"] = pd.to_datetime(data["DATA"], dayfirst=True, errors="coerce")

# Pega a última data por Kardex
ultimos = data.sort_values("DATA").groupby("KARDEX", as_index=False).last()

# Calcula diferença
ultimos["DIFERENÇA"] = ultimos["SISTEMA"] - ultimos["TOTAL"]

# Formatação da coluna Diferença
def formatar_seta(valor):
    if pd.isna(valor):
        return "—"
    if valor > 0:
        return f"↑ {int(valor)}"
    elif valor < 0:
        return f"↓ {abs(int(valor))}"
    else:
        return "0"

ultimos["DIFERENÇA"] = ultimos["DIFERENÇA"].apply(formatar_seta)

# Formata a data para dd/mm/aaaa
ultimos["DATA"] = ultimos["DATA"].dt.strftime("%d/%m/%Y")

# Seleciona e formata colunas
resultado = ultimos[["DATA", "KARDEX", "LUBRIFICANTE", "TOTAL", "SISTEMA", "DIFERENÇA"]]

# Exibir a tabela com estilo
st.write(
    resultado.style
        .format({
            "TOTAL": lambda x: f"{int(x)}" if pd.notna(x) else "—",
            "SISTEMA": lambda x: f"{int(x)}" if pd.notna(x) else "—",
            "KARDEX": lambda x: f"{int(x)}" if pd.notna(x) else "—"
        }, na_rep="—")
        .set_properties(subset=["KARDEX", "TOTAL", "SISTEMA"], **{'text-align': 'center'})
        .set_table_styles([dict(selector='th', props=[('text-align', 'center')])])
        .hide(axis="index")
        .to_html(),
    unsafe_allow_html=True,
)
