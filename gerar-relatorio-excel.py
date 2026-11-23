import sqlite3
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# 1. Conectar ao banco SQLite 
with sqlite3.connect('ecommerce.db') as conn:
    
    # Dicionário organizando as 5 consultas e os nomes das abas no Excel
    consultas = {
        "Faturamento_Real": """
            SELECT categoria_produto, COUNT(id_pedido) AS total_pedidos, ROUND(SUM(valor_total), 2) AS faturamento_real
            FROM vendas WHERE status_pedido = 'Entregue'
            GROUP BY categoria_produto ORDER BY faturamento_real DESC
        """,
        "Faturamento_Perdido": """
            SELECT categoria_produto, COUNT(id_pedido) AS total_pedidos, ROUND(SUM(valor_total), 2) AS faturamento_perdido
            FROM vendas WHERE status_pedido = 'Cancelado'
            GROUP BY categoria_produto ORDER BY faturamento_perdido DESC
        """,
        "Logistica_UF": """
            SELECT uf_destino, COUNT(id_pedido) AS total_pedidos, ROUND(AVG(valor_frete), 2) AS frete_medio, ROUND(AVG(prazo_entrega_dias), 1) AS prazo_medio_dias
            FROM vendas WHERE status_pedido = 'Entregue'
            GROUP BY uf_destino ORDER BY prazo_medio_dias DESC
        """,
        "Eficacia_Cupons": """
            SELECT cupom_desconto, COUNT(id_pedido) AS total_pedidos,
                   SUM(CASE WHEN status_pedido = 'Entregue' THEN 1 ELSE 0 END) AS pedidos_entregues,
                   SUM(CASE WHEN status_pedido = 'Cancelado' THEN 1 ELSE 0 END) AS pedidos_cancelados,
                   ROUND(AVG(valor_total), 2) AS ticket_medio
            FROM vendas GROUP BY cupom_desconto ORDER BY total_pedidos DESC
        """,
        "Sazonalidade_Mensal": """
            SELECT STRFTIME('%Y-%m', data_pedido) AS mes_ano, COUNT(id_pedido) AS total_pedidos, ROUND(SUM(valor_total), 2) AS faturamento_mensal
            FROM vendas WHERE status_pedido = 'Entregue'
            GROUP BY mes_ano ORDER BY mes_ano ASC
        """
    }

    arquivo_excel = "relatorio_executivo_ecommerce.xlsx"

    # 2. Exportar cada consulta para uma aba separada no Excel
    with pd.ExcelWriter(arquivo_excel, engine='openpyxl') as writer:
        for nome_aba, query in consultas.items():
            df = pd.read_sql_query(query, conn)
            df.to_excel(writer, sheet_name=nome_aba, index=False)

# 3. Formatação visual profissional com OpenPyXL
wb = load_workbook(arquivo_excel)
estilo_cabecalho = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid") # Azul escuro executivo
fonte_cabecalho = Font(color="FFFFFF", bold=True, size=11)

for aba in wb.sheetnames:
    ws = wb[aba]
    
    # Estilizar a linha 1 (cabeçalhos)
    for cell in ws[1]:
        cell.fill = estilo_cabecalho
        cell.font = fonte_cabecalho
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    # Ajustar automaticamente a largura de cada coluna para não cortar textos
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max_length + 5

wb.save(arquivo_excel)
print(f"Relatório '{arquivo_excel}' gerado e formatado com sucesso!")