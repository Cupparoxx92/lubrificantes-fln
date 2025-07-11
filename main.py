import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Estoque Lubrificantes", layout="wide")
st.title("🔍 Relatório Final por Óleo")

# URL da planilha
sheet_id = "1xbTqYab9lHWdYB-PD2Ma6d5B8YNZRUp7QK5JGT5trQI"
gid = "0"

# Leitura da planilha a partir da linha 903, com cabeçalho na primeira linha
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# Lê toda a planilha e depois filtra as linhas 
full_data = pd.read_csv(sheet_url, skiprows=902)

# Define os nomes das colunas corretamente (conforme sua planilha)
full_data.columns = ["Data", "Kardex", "Medida", "Galão", "Total", "Sistema", "Lubrificante"]

# Converte a coluna de data e numéricas
full_data["Data"] = pd.to_datetime(full_data["Data"], dayfirst=True, errors="coerce")
full_data["Total"] = pd.to_numeric(full_data["Total"], errors="coerce").fillna(0)
full_data["Sistema"] = pd.to_numeric(full_data["Sistema"], errors="coerce").fillna(0)

# Remove linhas sem Kardex ou Data válidos
full_data = full_data.dropna(subset=["Kardex", "Data"])

# Para cada Kardex, pega a última data
ultima_data = full_data.sort_values("Data").groupby("Kardex").tail(1)

# Calcula a diferença (Sistema - Total)
ultima_data["Diferença"] = ultima_data["Sistema"] - ultima_data["Total"]

# Seleciona e ordena as colunas desejadas
resultado_final = ultima_data[["Data", "Kardex", "Lubrificante", "Total", "Sistema", "Diferença"]]

# Exibe o DataFrame final
st.dataframe(resultado_final, use_container_width=True)
