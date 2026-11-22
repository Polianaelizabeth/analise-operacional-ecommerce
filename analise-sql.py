import pandas as pd
import sqlite3

df=pd.read_csv("vendas_ecommerce_limpo.csv")

conn = sqlite3.connect("ecommerce.db")

#conectando e criando tabela na base de dados

df.to_sql("vendas", conn, if_exists="replace", index=False)

print("banco 'ecommerce.db' criado e tabela 'vendas' carregada com sucesso!")

# faturamento real por categoria

query_faturamento = """
SELECT
    categoria_produto,
    COUNT(id_pedido) AS total_pedidos,
    ROUND(SUM(valor_total), 2) AS faturamento_real

FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY categoria_produto
ORDER BY faturamento_real desc

"""

df_faturamento = pd.read_sql_query(query_faturamento, conn)
print("--- FATURAMENTO REAL POR CATEGORIA ---")
print(df_faturamento)

# faturamento perdido por categoria

query_vendas_perdidas = """
SELECT
    categoria_produto,
    COUNT(id_pedido) AS total_pedidos,
    ROUND(SUM(valor_total), 2) AS faturamento_perdido

FROM vendas
WHERE status_pedido = 'Cancelado'
GROUP BY categoria_produto
ORDER BY faturamento_perdido desc

"""

df_faturamento_perdido = pd.read_sql_query(query_vendas_perdidas, conn)
print("--- FATURAMENTO PERDIDO POR CATEGORIA---")
print(df_faturamento_perdido)

# logistica por estado

query_logistica = """
    SELECT uf_destino,
    COUNT(id_pedido) AS total_pedidos, 
    ROUND(AVG(valor_frete), 2) AS media_frete,
    ROUND(AVG(prazo_entrega_dias), 1) AS media_dias_envio
    
    FROM vendas
    WHERE status_pedido = 'Entregue'
    GROUP BY uf_destino
    ORDER BY media_dias_envio desc

"""
df_logistica = pd.read_sql_query(query_logistica, conn)
print("----DESENPENHO LOGISTICO POR ESTADO---")
print(df_logistica)

# Eficácia de Cupons de Desconto 
query_cupons = """
SELECT 
    cupom_desconto,
    COUNT(id_pedido) AS total_pedidos,
    SUM(CASE WHEN status_pedido = 'Entregue' THEN 1 ELSE 0 END) AS pedidos_entregues,
    SUM(CASE WHEN status_pedido = 'Cancelado' THEN 1 ELSE 0 END) AS pedidos_cancelados,
    ROUND(AVG(valor_total), 2) AS ticket_medio
FROM vendas
GROUP BY cupom_desconto
ORDER BY total_pedidos DESC
"""

df_cupons = pd.read_sql_query(query_cupons, conn)
print("\n--- EFICÁCIA DE CUPONS ---")
print(df_cupons)

# Sazonalidade Mensal (Faturamento Real)
query_sazonalidade = """
SELECT 
    STRFTIME('%Y-%m', data_pedido) AS mes_ano,
    COUNT(id_pedido) AS total_pedidos,
    ROUND(SUM(valor_total), 2) AS faturamento_mensal
FROM vendas
WHERE status_pedido = 'Entregue'
GROUP BY mes_ano
ORDER BY mes_ano ASC
"""

df_sazonalidade = pd.read_sql_query(query_sazonalidade, conn)
print("\n--- SAZONALIDADE MENSAL ---")
print(df_sazonalidade)

# Fechando a conexão com o banco de dados
conn.close()