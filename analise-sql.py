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