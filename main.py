import pandas as pd

# Simulação dos dados (pode trocar depois por leitura do Google Sheets)
data = pd.DataFrame({
    "KARDEX": [40300012, 40300040],
    "LUBRIFICANTE": ["OLEO (RETARDER) ATF DEXRON III", "ANTI CORROSIVO ORGANICO LARANJA"],
    "TOTAL": [150, 90],
    "SISTEMA": [130, 100]
})

# Calcula diferença e acuracidade
data["DIFERENCA"] = data["TOTAL"] - data["SISTEMA"]
data["ACURACIDADE"] = ((data["TOTAL"] / data["SISTEMA"]) * 100).round(1).astype(str) + "%"

# Gera o HTML base
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
.card { width: 100%; margin-bottom: 20px; border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); background-color: white; }
.bar-container { height: 20px; background-color: #ddd; margin-bottom: 8px; border-radius: 4px; overflow: hidden; }
.bar-fisico { background-color: blue; height: 100%; color: white; text-align: center; }
.bar-sistema { background-color: orange; height: 100%; color: white; text-align: center; }
</style>
</head>
<body>

<h2 style="text-align: center;">Relatório - Última Atualização</h2>

<div style="display: flex; justify-content: space-between;">

    <!-- Tabela -->
    <div style="width: 60%; padding-right: 20px;">
        <table>
        <tr>
            <th>KARDEX</th>
            <th>LUBRIFICANTE</th>
            <th>TOTAL</th>
            <th>SISTEMA</th>
            <th>DIFERENÇA</th>
            <th>ACURACIDADE</th>
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

# Gera as linhas da tabela
tabela_html = ""
for _, row in data.iterrows():
    cor = 'green' if row['DIFERENCA'] > 0 else 'red' if row['DIFERENCA'] < 0 else 'black'
    tabela_html += f"<tr><td>{row['KARDEX']}</td><td>{row['LUBRIFICANTE']}</td><td>{row['TOTAL']}</td><td>{row['SISTEMA']}</td><td style='color:{cor}'>{row['DIFERENCA']}</td><td>{row['ACURACIDADE']}</td></tr>"

# Gera os cards laterais
cards_html = ""
for _, row in data.iterrows():
    max_value = max(row["TOTAL"], row["SISTEMA"])
    fisico_percent = int(row["TOTAL"] / max_value * 100)
    sistema_percent = int(row["SISTEMA"] / max_value * 100)

    cards_html += f"""
    <div class='card'>
        <strong>{row['KARDEX']} - {row['LUBRIFICANTE']}</strong><br><br>
        <div class='bar-container'>
            <div class='bar-fisico' style='width:{fisico_percent}%'>{row['TOTAL']} L (Físico)</div>
        </div>
        <div class='bar-container'>
            <div class='bar-sistema' style='width:{sistema_percent}%'>{row['SISTEMA']} L (Sistema)</div>
        </div>
        Diferença: <strong style='color:{'green' if row['DIFERENCA'] > 0 else 'red' if row['DIFERENCA'] < 0 else 'black'}'>{row['DIFERENCA']}</strong><br>
        Acuracidade: {row['ACURACIDADE']}
    </div>
    """

# Substitui as tags no HTML
html = html.replace("{%TABELA_ROWS%}", tabela_html).replace("{%CARDS%}", cards_html)

# Salva no arquivo
temp_html_file = "relatorio.html"
with open(temp_html_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Arquivo HTML gerado: {temp_html_file}")
