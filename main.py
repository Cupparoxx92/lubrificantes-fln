import pandas as pd
import math
import unicodedata

def normalizar_colunas(df):
    # Remove acentos, espaços extras e coloca tudo minúsculo
    def normalize(col):
        col = col.strip().lower()
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
        return col
    df.columns = [normalize(col) for col in df.columns]
    return df

def calcular_totais(contabil):
    # Atenção aos nomes padronizados das colunas
    valor_fisico = contabil["r fisico"].sum()
    valor_sistema = contabil["r sistema"].sum()
    diferenca_contabil = abs(valor_fisico - valor_sistema)
    sobras = contabil["faltas"].apply(lambda x: x if x > 0 else 0).sum()
    faltas = contabil["faltas"].apply(lambda x: x if x < 0 else 0).sum()
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
        fisico = row["total"]
        sistema = row["sistema"]
        diferenca = fisico - sistema
        max_value = max(fisico, sistema, 1)
        acuracidade = round((min(fisico, sistema) / max_value) * 100, 2)
        cards_html += f"""
        <div style='border: 1px solid #ddd; border-radius: 8px; padding: 8px; margin-bottom: 12px; min-width:330px; max-width:370px; display:inline-block; margin-right:12px;'>
            <strong>{row['kardex']} - {row['lubrificante']}</strong><br>
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
    # URLs das abas
    url_contabil = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=879658789&single=true&output=csv"
    url_lubrificantes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyYi-89V_kh3Ts43iBWAfi8D7vylA6BsiQwlmG0xZqnoUcPKaPGbL6e3Qrie0SoqVZP64nRRQu71Z2/pub?gid=0&single=true&output=csv"

    contabil = pd.read_csv(url_contabil)
    lubrificantes = pd.read_csv(url_lubrificantes)

    contabil = normalizar_colunas(contabil)
    lubrificantes = normalizar_colunas(lubrificantes)

    # Exemplo para debug se necessário:
    # print(contabil.columns)
    # print(lubrificantes.columns)

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
