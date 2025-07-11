import pandas as pd

# Simulação da leitura dos dados
data = pd.DataFrame({
    "KARDEX": [40300012, 40300040],
    "LUBRIFICANTE": ["OLEO (RETARDER) ATF DEXRON III", "ANTI CORROSIVO ORGANICO LARANJA"],
    "TOTAL": [150, 90],
    "SISTEMA": [130, 100]
})

# Calcula a diferença e a acuracidade
data["DIFERENCA"] = data["TOTAL"] - data["SISTEMA"]
data["ACURACIDADE"] = ((data["TOTAL"] / data["SISTEMA"]) * 100).round(1).astype(str) + "%"

# Gera HTML
html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Relatório de Acuracidade</title>
<style>
body { font-family: Arial; margin: 20px; }
table { border-collapse: collapse; width: 60%; float: left; margin-right: 20px; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
th { background-color: #f2f2f2; }
.card { width: 30%; margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
.bar-container { height: 20px; background-color: #ddd; margin-bottom: 5px; }
.bar-fisico { background-color: blue; height: 100%; color: white; text-align: center; }
.bar-sistema { background-color: orange; height: 100%; color: white; text-align: center; }
</style>
</head>
<body>

<h2>Relatório - Última Atualização</h2>

<table>
<tr>
<th>KARDEX</th>
<th>LUBRIFICANTE</th>
<th>TOTAL</th>
<th>SISTEMA</th>
<th>DIFERENÇA</th>
<th>ACURACIDADE</th>
</tr>
"""

# Adiciona as linhas da tabela
for _, row in data.iterrows():
    cor = 'green' if row['DIFERENCA'] > 0 else 'red' if row['DIFERENCA'] < 0 else 'black'
    html += f"<tr><td>{row['KARDEX']}</td><td>{row['LUBRIFICANTE']}</td><td>{row['TOTAL']}</td><td>{row['SISTEMA']}</td><td style='color:{cor}'>{row['DIFERENCA']}</td><td>{row['ACURACIDADE']}</td></tr>"

html += "</table>"

# Adiciona os cards com barras
for _, row in data.iterrows():
    max_value = max(row["TOTAL"], row["SISTEMA"])
    fisico_percent = int(row["TOTAL"] / max_value * 100)
    sistema_percent = int(row["SISTEMA"] / max_value * 100)

    html += f"""
    <div class='card'>
        <strong>{row['KARDEX']} - {row['LUBRIFICANTE']}</strong><br><br>
        <div class='bar-container'>
            <div class='bar-fisico' style='width:{fisico_percent}%'>{row['TOTAL']} L (Físico)</div>
        </div>
        <div class='bar-container'>
            <div class='bar-sistema' style='width:{sistema_percent}%'>{row['SISTEMA']} L (Sistema)</div>
        </div>
        Diferença: <strong style='color:{'green' if row['DIFERENCA']>0 else 'red' if row['DIFERENCA']<0 else 'black'}'>{row['DIFERENCA']}</strong><br>
        Acuracidade: {row['ACURACIDADE']}
    </div>
    """

html += "</body></html>"

# Salva no arquivo
temp_html_file = "relatorio.html"
with open(temp_html_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Arquivo HTML gerado: {temp_html_file}")
