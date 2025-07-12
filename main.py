import pandas as pd

# Dados de exemplo (substitua pela leitura do seu Google Sheets)
valor_fisico = 135622
valor_sistema = 135133
diferenca_contabil = 489.81
sobras = 1548.63
faltas = -1058.81
acuracidade_contabil = round((min(valor_fisico, valor_sistema) / max(valor_fisico, valor_sistema)) * 100, 2)

# Define a cor do arco com base na meta
meta = 99.98
cor = "blue" if acuracidade_contabil >= meta else "red"

# Calcula o percentual do arco (limitado a 100)
percentual_arc = min(acuracidade_contabil, 100)

# Monta o HTML com espaço ajustado e meta no gráfico
html = f"""
<div style="display: flex; justify-content: flex-start; align-items: center; gap: 80px; margin-bottom: 20px;">

  <!-- Tabela de resumo contábil -->
  <table style="width: 400px; background-color: #cfe2f3; border-collapse: collapse;">
      <tr><th colspan="2" style="padding: 8px; border: 1px solid #ddd;">ACURACIDADE CONTÁBIL</th></tr>
      <tr><td style="padding: 6px; border: 1px solid #ddd;">VALOR FÍSICO</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {valor_fisico:,.2f}</td></tr>
      <tr><td style="padding: 6px; border: 1px solid #ddd;">VALOR SISTEMA</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {valor_sistema:,.2f}</td></tr>
      <tr><td style="padding: 6px; border: 1px solid #ddd;">DIFERENÇA CONTÁBIL</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {diferenca_contabil:,.2f}</td></tr>
      <tr><td style="padding: 6px; border: 1px solid #ddd;">(+)Sobras</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {sobras:,.2f}</td></tr>
      <tr><td style="padding: 6px; border: 1px solid #ddd;">(-)Faltas</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {faltas:,.2f}</td></tr>
  </table>

  <!-- Gráfico -->
  <svg width="200" height="120">
      <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#ddd" stroke-width="15" />
      <path d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="{cor}"
            stroke-width="15"
            stroke-dasharray="{percentual_arc} 100"
            stroke-dashoffset="0"
            transform="rotate(-180 100 100)" />
      <text x="100" y="65" text-anchor="middle" font-size="20" font-weight="bold">{acuracidade_contabil:.2f}%</text>
      <text x="100" y="90" text-anchor="middle" font-size="12" font-weight="bold">R$ {diferenca_contabil:,.2f}</text>
      <text x="100" y="115" text-anchor="middle" font-size="10" fill="#555">Meta: 99,98%</text>
  </svg>

</div>
"""

# Salva o HTML em um arquivo
with open("relatorio.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Relatório gerado: relatorio.html")
