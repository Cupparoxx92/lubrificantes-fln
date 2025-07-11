import pandas as pd

# Link da planilha publicada no formato CSV
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

# Lê a planilha completa
df = pd.read_csv(sheet_url, header=None)

# Seleciona as colunas A (0), B (1), E (4), F (5), G (6)
df = df[[0, 1, 4, 5, 6]]
df.columns = ["DATA", "KARDEX", "TOTAL", "SISTEMA", "LUBRIFICANTE"]

# Remove linhas vazias em KARDEX, TOTAL, SISTEMA
df = df.dropna(subset=["KARDEX", "TOTAL", "SISTEMA"])

# Converte TOTAL e SISTEMA para inteiro
df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce").fillna(0).astype(int)
df["SISTEMA"] = pd.to_numeric(df["SISTEMA"], errors="coerce").fillna(0).astype(int)

# Converte a data
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")

# Pega a última data de cada Kardex
ultimos = df.sort_values("DATA").groupby("KARDEX", as_index=False).last()

# Calcula diferença
ultimos["DIFERENCA"] = ultimos["TOTAL"] - ultimos["SISTEMA"]

# Calcula a acuracidade (mantém nos cards)
ultimos["ACURACIDADE"] = (
    (ultimos[["TOTAL", "SISTEMA"]].min(axis=1) / ultimos[["TOTAL", "SISTEMA"]].max(axis=1))
    .fillna(0)
    .round(2) * 100
).astype(str) + "%"

# ---------------------- HTML ----------------------

html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Relatório de Acuracidade</title>
<style>
body { font-family: Arial; margin: 20px; background-color: #f9f9f9; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
th { background-color: #e0e0e0; color: #333; }

.card { width: 100%; margin-bottom: 12px; border: 1px solid #ddd; padding: 10px; border-radius: 8px; background-color: white; font-size: 13px; }

.bar-container { height: 16px; background-color: #ddd; margin-bottom: 6px; border-radius: 4px; overflow: hidden; }
.bar-fisico { background-color: blue; height: 100%; color: white; text-align: center; font-size: 11px; }
.bar-sistema { background-color: orange; height: 100%; color: white; text-align: center; font-size: 11px; }
</style>
</head>
<body>

<h2 style="text-align: center;">Relatório - Última Atualização por Lubrificante</h2>

<div style="display: flex; justify-content: space-between; align-items: flex-start;">

    <!-- Tabela -->
    <div style="width: 60%; padding-right: 20px;">
        <table>
        <tr>
            <th>KARDEX</th>
            <th>LUBRIFICANTE</th>
            <th>TOTAL</th>
            <th>SISTEMA</th>
            <th>DIFERENÇA</th>
        </tr>
        {%TABELA_ROWS%}
        </table>
    </div>

    <!-- Cards -->
    <div style="width: 35%;">
        {%CARDS%}
    </div>

</div>

</body>
</html>
"""

# Monta as linhas da tabela
tabela_html = ""
for _, row in ultimos.iterrows():
    cor = 'green' if row['DIFERENCA'] > 0 else 'red' if row['DIFERENCA'] < 0 else 'black'
    tabela_html += f"<tr><td>{row['KARDEX']}</td><td>{row['LUBRIFICANTE']}</td><td>{row['TOTAL']}</td><td>{row['SISTEMA']}</td><td style='color:{cor}'>{row['DIFERENCA']}</td></tr>"

# Monta os cards
cards_html = ""
for _, row in ultimos.iterrows():
    max_value = max(row["TOTAL"], row["SISTEMA"]) if max(row["TOTAL"], row["SISTEMA"]) != 0 else 1
    fisico_percent = int(row["TOTAL"] / max_value * 100)
    sistema_percent = int(row["SISTEMA"] / max_value * 100)

    cards_html += f"""
    <div class='card'>
        <strong>{row['KARDEX']} - {row['LUBRIFICANTE']}</strong><br>
        <div class='bar-container'>
            <div class='bar-fisico' style='width:{fisico_percent}%'>{row['TOTAL']} L (Físico)</div>
        </div>
        <div class='bar-container'>
            <div class='bar-sistema' style='width:{sistema_percent}%'>{row['SISTEMA']} L (Sistema)</div>
        </div>
        <div>
            Diferença: <strong style='color:{'green' if row['DIFERENCA'] > 0 else 'red' if row['DIFERENCA'] < 0 else 'black'}'>{row['DIFERENCA']}</strong> |
            Acuracidade: {row['ACURACIDADE']}
        </div>
    </div>
    """

# Substitui no HTML
html = html.replace("{%TABELA_ROWS%}", tabela_html).replace("{%CARDS%}", cards_html)

# Salva no arquivo
with open("relatorio.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Relatório gerado: relatorio.html")
