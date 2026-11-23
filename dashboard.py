import sqlite3
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Dashboard Operacional E-commerce", page_icon="📊", layout="wide")

st.title("📊 Painel Operacional e Financeiro — E-commerce")
st.markdown("Análise de faturamento, cancelamentos, logística e sazonalidade.")

# Carregar dados do banco SQLite
with sqlite3.connect("ecommerce.db") as conn:
    df = pd.read_sql_query("SELECT * FROM vendas", conn)

# Barra lateral com filtros
st.sidebar.header("Filtros")
categorias = st.sidebar.multiselect(
    "Categoria do Produto:",
    options=df["categoria_produto"].unique(),
    default=df["categoria_produto"].unique()
)
status = st.sidebar.multiselect(
    "Status do Pedido:",
    options=df["status_pedido"].unique(),
    default=df["status_pedido"].unique()
)

df_filtrado = df[(df["categoria_produto"].isin(categorias)) & (df["status_pedido"].isin(status))]

# KPIs Principais
faturamento_real = df_filtrado[df_filtrado["status_pedido"] == "Entregue"]["valor_total"].sum()
faturamento_perdido = df_filtrado[df_filtrado["status_pedido"] == "Cancelado"]["valor_total"].sum()
total_pedidos = len(df_filtrado)
prazo_medio = df_filtrado["prazo_entrega_dias"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Entregue", f"R$ {faturamento_real:,.2f}")
col2.metric("Receita Perdida (Cancelados)", f"R$ {faturamento_perdido:,.2f}")
col3.metric("Total de Pedidos", f"{total_pedidos}")
col4.metric("Prazo Médio de Entrega", f"{prazo_medio:.1f} dias")

st.divider()

# Gráficos em duas colunas
g1, g2 = st.columns(2)

with g1:
    st.subheader("Faturamento por Categoria (R$)")
    fat_cat = df_filtrado.groupby("categoria_produto")["valor_total"].sum().sort_values(ascending=False)
    st.bar_chart(fat_cat)

with g2:
    st.subheader("Prazo Médio de Entrega por Estado (Dias)")
    log_uf = df_filtrado.groupby("uf_destino")["prazo_entrega_dias"].mean().sort_values(ascending=False)
    st.bar_chart(log_uf)

# Gráfico de Sazonalidade Mensal
st.subheader("Evolução Mensal de Faturamento (R$)")
df_filtrado = df_filtrado.copy()
df_filtrado["mes_ano"] = df_filtrado["data_pedido"].str.slice(0, 7)
sazonalidade = df_filtrado.groupby("mes_ano")["valor_total"].sum()
st.line_chart(sazonalidade)