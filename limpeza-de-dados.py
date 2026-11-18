import pandas as pd

df = pd.read_csv("vendas_ecommerce_bruto.csv")

# carregando e visualizando base de dados
print(df.head(15))
print("--valores antes da limpeza--")
print("total de linhas e colunas:", df.shape)
print("valores nulos por coluna:", df.isnull().sum())
print("total de linhas duplicadas:", df.duplicated().sum())

# excluindo linhas duplicadas
df = df.drop_duplicates()

# padronozação de textos
df["categoria_produto"] = df["categoria_produto"].str.strip().str.title()
df["status_pedido"] = df["status_pedido"].str.strip().str.title()
df["cupom_desconto"] = df["cupom_desconto"].str.strip()
df["uf_destino"] = df["uf_destino"].str.strip().str.upper()

# padronização de datas
df["data_pedido"] = pd.to_datetime(df["data_pedido"], dayfirst= True, format= "mixed") 

# tratando valores nulos. Como visto no print "valores nulos por coluna:", a unica coluna com valores nulos é a valor_frete. Então vamos tratá-las de duas maneiras: onde tem cumpom de frete grátis, será colocado o valor 0.0. onde não tem o cumpom será colocado uma mediana do frete daquela UF

print(df["cupom_desconto"].value_counts())
df.loc[df["cupom_desconto"] == "FRETEGRATIS", "valor_frete"] = df["valor_frete"].fillna(0.0)
df["valor_frete"] = df["valor_frete"].fillna(df.groupby("uf_destino")["valor_frete"].transform("median"))

# adicionando coluna de valor total: produto mais frete
df["valor_total"] = (df["valor_frete"] + df["valor_produto"]).round(2)

# visualizando dados depos da limpeza

print(df.head(15))
print("--valores depois da limpeza--")
print("total de linhas e colunas:", df.shape)
print("valores nulos por coluna:", df.isnull().sum())
print("total de linhas duplicadas:", df.duplicated().sum())

df.to_csv("vendas_ecommerce_limpo.csv", index=False)
print("arquivo 'vendas_ecommerce_limpo.csv' salvo com sucesso!")