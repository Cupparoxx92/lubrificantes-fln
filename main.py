import pandas as pd
import math

def calcular_totais(contabil):
    valor_fisico = contabil["R$ fisico"].sum()
    valor_sistema = contabil["R$ sistema"].sum()
    diferenca_contabil = abs(valor_fisico - valor_sistema)
    sobras = contabil["Faltas"].apply(lambda x: x if x > 0 else 0).sum()
    faltas = contabil["Faltas"].apply(lambda x: x if x < 0 else 0).sum()
    acuracidade_contabil = round((min(valor_fisico, valor_sistema) / max(valor_fisico, valor_sistema)) * 100, 2)
    return valor_fisico, valor_sistema, diferenca_contabil, sobras, faltas, acuracidade_contabil

def gerar_grafico(acuracidade_contabil, diferenca_contabil):
    meta = 99.98
    cor = "#00BFFF" if acuracidade_contabil >= meta else "#FF4C4C"
    percentual_arc = min(acuracidade_contabil, 100)
    end_x = 150 + 100 * math.cos(math.radians(180 - percentual_arc * 1.8))
    end_y = 150 - 100 * math.sin(math.radians(percentual_arc * 1.8))
    large_arc_flag = 1 if percentual_arc > 50 else 0

    return f"""
    <svg width="300" height="160">
        <circle cx="150" cy="150" r="100" fill="none" stroke="#ddd" stroke-width="20" />
        <path d="M 50 150 A 100 100 0 {large_arc_flag} 1 {end_x:.2f} {end_y:.2f}" fill="none" stroke="{cor}" stroke-width="20" />
        <text x="150" y="90" text-anchor="middle" font-size="28" font-weight="bold" fill="{cor}">{acuracidade_contabil:.2f}%</text>
        <text x="150" y="115" text-anchor="middle" font-size="14" fill="#000">R$ {diferenca_contabil:,.2f}</text>
        <text x="150" y="140" text-anchor="middle" font-size="12" fill="#555">Meta: 99,98%</text>
    </svg>
    """

def gerar_tabela(valor_fisico, valor_sistema, diferenca_contabil, sobras, faltas):
    return f"""
    <table style="width: 400px; background-color: #cfe2f3; border-collapse: collapse;">
        <tr><th colspan="2" style="padding: 8px; border: 1px solid #ddd;">ACURACIDADE CONTÁBIL</th></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">VALOR FÍSICO</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {valor_fisico:,.2f}</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">VALOR SISTEMA</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {valor_sistema:,.2f}</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">DIFERENÇA CONTÁBIL</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {diferenca_contabil:,.2f}</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">(+)Sobras</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {sobras:,.2f}</td></tr>
        <tr><td style="padding: 6px; border: 1px solid #ddd;">(-)Faltas</td><td style="padding: 6px; border: 1px solid #ddd;">R$ {faltas:,.2f}</td></tr>
    </table>
    """

def gerar_cards(lubrificantes):
    cards_html = ""
    for _, row in lubrificantes.iterrows():
        fisico = row["TOTAL"]
        sistema = row["SISTEMA"]
        diferenca = fisico - sistema
        max_value = max(fisico, sistema, 1)
        acuracidade = round((min(fisico, sistema) / max_value) * 100, 2)

        cards_html += f"""
        <div style='border: 1px solid #ddd; border-radius: 8px; padding: 8px; margin-bottom: 12px;'>
            <strong>{row['KARDEX']} - {row['LUBRIFICANTE']}</strong><br>
            Físico: {fisico} | Sistema: {sistema}<br>
            Diferença: {diferenca} | Acuracidade: {acuracidade}%
        </div>
        """
    return cards_html

def gerar_html(tabela, grafico, cards):
    return f"""
    <div style="display: flex; justify-content: flex-start; align-items: center; gap: 80px; margin-bottom: 20px;">
        {tabela}
        {grafico}
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 16px;">
        {cards}
    </div>
    """

def main():
    contabil = pd.DataFrame({
        "Kardex": [40300023, 40300012, 40309451],
        "litros_diferenca": [-38, 0, 37],
        "R$ fisico": [32266.25, 2300.44, 8740.32],
        "R$ sistema": [33045.21, 2299.24, 8198.46],
        "Divergencia %": [-2.36, 0.05, 6.61],
        "R$": [-778.96, 1.20, 541.85],
        "Faltas": [-1058.81, 0, 1548.63]
    })

    lubrificantes = pd.DataFrame({
        "KARDEX": [40300023, 40300012, 40309451],
        "LUBRIFICANTE": ["Óleo Motor", "Óleo Transmissão", "Óleo Hidráulico"],
        "TOTAL": [150, 90, 75],
        "SISTEMA": [130, 100, 80]
    })

    valor_fisico, valor_sistema, diferenca_contabil, sobras, faltas, acuracidade_contabil = calcular_totais(contabil)

    tabela = gerar_tabela(valor_fisico, valor_sistema, diferenca_contabil, sobras, faltas)
    grafico = gerar_grafico(acuracidade_contabil, diferenca_contabil)
    cards = gerar_cards(lubrificantes)

    html = gerar_html(tabela, grafico, cards)

    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Relatório gerado: relatorio.html")

if __name__ == "__main__":
    main()
