import pandas as pd

# --------- Leitura da aba de ACURACIDADE CONTÁBIL ----------
contabil_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=879658789&single=true&output=csv"
contabil = pd.read_csv(contabil_url, header=None, skiprows=13)

# Remove linhas vazias
contabil = contabil.dropna(subset=[0])

# Converte valores para número (remove R$ e pontos)
def clean_money(value):
    if pd.isna(value):
        return 0
    return pd.to_numeric(str(value).replace("R$", "").replace(".", "").replace(",", ".").replace(" ", "").replace("-", ""), errors="coerce") * (-1 if "-" in str(value) else 1)

# Soma os campos
valor_fisico = contabil[2].apply(clean_money).sum()
valor_sistema = contabil[3].apply(clean_money).sum()
diferenca_contabil = contabil[5].apply(clean_money).sum()

# Sobras e faltas da coluna G (índice 6)
sobras = contabil[6].dropna().apply(lambda x: clean_money(x) if "Sobra" not in str(x) else 0).sum()
faltas = contabil[6].dropna().apply(lambda x: clean_money(x) if "-" in str(x) else 0).sum()

# Acuracidade contábil
acuracidade_contabil = round((min(valor_fisico, valor_sistema) / max(valor_fisico, valor_sistema)) * 100, 2) if max(valor_fisico, valor_sistema) else 0

# ---------- Leitura da aba dos LUBRIFICANTES ----------
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"
df = pd.read_csv(sheet_url, header=None)
df = df[[0, 1, 4, 5, 6]]
df.columns = ["DATA", "KARDEX", "TOTAL", "SISTEMA", "LUBRIFICANTE"]
df = df.dropna(subset=["KARDEX", "TOTAL", "SISTEMA"])
df = df[df["KARDEX"].apply(lambda x: str(x).isdigit())]
df["TOTAL"] = pd.to_numeric(df["TOTAL"], errors="coerce").fillna(0).astype(int)
df["SISTEMA"] = pd.to_numeric(df["SISTEMA"], errors="coerce").fillna(0).astype(int)
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
ultimos = df.sort_values("DATA").groupby("KARDEX", as_index=False).last()
ultimos["DIFERENCA"] = ultimos["TOTAL"] - ultimos["SISTEMA"]
ultimos["ACURACIDADE"] = (ultimos[["TOTAL", "SISTEMA"]].min(axis=1) / ultimos[["TOTAL", "SISTEMA"]].max(axis=1)).fillna(0).round(2) * 100
ultimos["ACURACIDADE"] = ultimos["ACURACIDADE"].astype(str) + "%"

# ---------- Monta o HTML ----------

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

.contabil-card { background-color: #cfe2f3; padding: 15px; border-radius: 8px; margin-bottom: 20px; width: 400px; }
.contabil-card h3 { text-align: center; }

.card { width: 100%; margin-bottom: 12px; border: 1px solid #ddd; padding: 10px; border-radius: 8px; background-color: white; font-size: 13px; }
.bar-container { height: 16px; background-color: #ddd; margin-bottom: 6px; border-radius: 4px; overflow: hidden; }
.bar-fisico { background-color: blue; height: 100%; color: white; text-align: center; font-size: 11px; }
.bar-sistema { background-color: orange; height: 100%; color: white; text-align: center; font-size: 11px; }
</style>
</head>
<body>

<!-- Card Azul -->
<div class="contabil-card">
<h3>ACURACIDADE CONTÁBIL</h3>
VALOR FÍSICO: R$ {valor_fisico:,.2f}<br>
VALOR SISTEMA: R$ {valor_sistema:,.2f}<br>
DIFERENÇA CONTÁBIL: R$ {diferenca_contabil:,.2f}<br>
(+)Sobras: R$ {sobras:,.2f}<br>
(-)Faltas: R$ {faltas:,.2f}<br>
ACURACIDADE CONTÁBIL: {acuracidade_contabil:.2f}%
</div>

<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div style="width: 60%; padding-right: 20px;">
<table>
<tr><th>DATA</th><th>KARDEX</th><th>LUBRIFICANTE</th><th>TOTAL</th><th>SISTEMA</th><th>DIFERENÇA</th></tr>
{%TABELA_ROWS%}
</table>
</div>

<div style="width: 35%;">
{%CARDS%}
</div>
</div>
</body>
</html>
""".format(
    valor_fisico=valor_fisico,
    valor_sistema=valor_sistema,
    diferenca_contabil=diferenca_contabil,
    sobras=sobras,
    faltas=faltas,
    acuracidade_contabil=acuracidade_contabil,
)

# Monta a tabela
tabela_html = ""
for _, row in ultimos.iterrows():
    cor = 'green' if row['DIFERENCA'] > 0 else 'red' if row['DIFERENCA'] < 0 else 'black'
    data_str = row['DATA'].strftime('%d/%m/%Y') if pd.notnull(row['DATA']) else '-'
    tabela_html += f"<tr><td>{data_str}</td><td>{row['KARDEX']}</td><td>{row['LUBRIFICANTE']}</td><td>{row['TOTAL']}</td><td>{row['SISTEMA']}</td><td style='color:{cor}'>{row['DIFERENCA']}</td></tr>"

# Monta os cards laterais
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
            Diferença: <strong style='color:{cor}'>{row['DIFERENCA']}</strong> |
            Acuracidade: {row['ACURACIDADE']}
        </div>
    </div>
    """

# Substitui no HTML
html = html.replace("{%TABELA_ROWS%}", tabela_html).replace("{%CARDS%}", cards_html)

# Salva o arquivo
with open("relatorio.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Relatório gerado: relatorio.html")
