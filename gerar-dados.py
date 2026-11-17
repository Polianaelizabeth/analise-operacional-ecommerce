"""
Gerador de dataset fictício: operação comercial e logística de e-commerce nacional.
Saída: vendas_ecommerce_bruto.csv (1.000 pedidos únicos + 30 linhas duplicadas = 1.030 linhas)

Dependências: pandas, numpy
"""

from datetime import date, timedelta

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Configurações
# ----------------------------------------------------------------------------
SEED = 42
N_PEDIDOS = 1000          # pedidos únicos
N_DUPLICADAS = 30         # linhas duplicadas inseridas propositalmente
PCT_FRETE_NULO = 0.05     # 5% de valor_frete nulo
ARQUIVO_SAIDA = "vendas_ecommerce_bruto.csv"

rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------------
# Parâmetros de negócio
# ----------------------------------------------------------------------------
UFS = ["SP", "RJ", "MG", "DF", "GO", "PR", "BA", "RS", "SC", "PE"]
PESO_UF = [0.30, 0.12, 0.12, 0.06, 0.07, 0.08, 0.07, 0.07, 0.05, 0.06]

# Faixa de frete (R$) e de prazo (dias) por UF: (min, max)
FRETE_UF = {
    "SP": (12, 25), "RJ": (18, 30), "MG": (18, 32), "DF": (25, 40), "GO": (25, 40),
    "PR": (22, 35), "SC": (25, 38), "RS": (28, 45), "BA": (35, 58), "PE": (38, 62),
}
PRAZO_UF = {
    "SP": (1, 5), "RJ": (2, 7), "MG": (2, 8), "DF": (4, 10), "GO": (4, 10),
    "PR": (3, 9), "SC": (3, 10), "RS": (5, 12), "BA": (7, 16), "PE": (8, 18),
}

# Categoria -> (mediana do valor, sigma lognormal, mínimo, máximo)
CATEGORIAS = {
    "Eletrônicos":       (900, 0.80, 150, 6500),
    "Perfumaria":        (180, 0.55, 40, 700),
    "Casa e Decoração":  (220, 0.75, 30, 1800),
    "Acessórios":        (90, 0.60, 20, 600),
    "Moda":              (160, 0.55, 40, 900),
}
PESO_CATEGORIA = [0.22, 0.18, 0.22, 0.18, 0.20]

# Multiplicador de frete por categoria (produtos maiores/mais pesados custam mais)
FATOR_FRETE_CAT = {
    "Eletrônicos": 1.15, "Perfumaria": 0.90, "Casa e Decoração": 1.30,
    "Acessórios": 0.85, "Moda": 0.90,
}

CUPONS = ["Sem Cupom", "BEMVINDO10", "FRETEGRATIS", "VIP20"]
PESO_CUPOM = [0.55, 0.20, 0.15, 0.10]

# ----------------------------------------------------------------------------
# Geração das colunas
# ----------------------------------------------------------------------------
hoje = date.today()
inicio = hoje - timedelta(days=182)  # ~6 meses

# Datas: ordenadas para que id_pedido seja cronológico
offsets = np.sort(rng.integers(0, (hoje - inicio).days + 1, size=N_PEDIDOS))
datas = pd.to_datetime([inicio + timedelta(days=int(o)) for o in offsets])

# id_pedido
ids = [f"PED-{i:04d}" for i in range(1, N_PEDIDOS + 1)]

# UF e categoria
ufs = rng.choice(UFS, size=N_PEDIDOS, p=PESO_UF)
cats = rng.choice(list(CATEGORIAS.keys()), size=N_PEDIDOS, p=PESO_CATEGORIA)

# valor_produto (lognormal por categoria, limitado à faixa realista)
valores = np.empty(N_PEDIDOS)
for i, c in enumerate(cats):
    mediana, sigma, vmin, vmax = CATEGORIAS[c]
    v = rng.lognormal(mean=np.log(mediana), sigma=sigma)
    valores[i] = np.clip(v, vmin, vmax)
valores = np.round(valores, 2)

# cupom
cupons = rng.choice(CUPONS, size=N_PEDIDOS, p=PESO_CUPOM)

# valor_frete (por região, fator da categoria; FRETEGRATIS zera o frete)
fretes = np.empty(N_PEDIDOS)
for i, (uf, c) in enumerate(zip(ufs, cats)):
    fmin, fmax = FRETE_UF[uf]
    fretes[i] = rng.uniform(fmin, fmax) * FATOR_FRETE_CAT[c]
fretes = np.round(fretes, 2)
fretes[cupons == "FRETEGRATIS"] = 0.0

# prazo_entrega_dias (inteiro entre 1 e 18, conforme UF)
prazos = np.array(
    [rng.integers(PRAZO_UF[uf][0], PRAZO_UF[uf][1] + 1) for uf in ufs]
).clip(1, 18)

# status_pedido (coerente com a idade do pedido)
status = []
for d in datas:
    idade = (pd.Timestamp(hoje) - d).days
    if idade <= 7:
        probs = [0.15, 0.05, 0.00, 0.80]   # quase tudo ainda em trânsito
    elif idade <= 20:
        probs = [0.55, 0.08, 0.02, 0.35]
    else:
        probs = [0.82, 0.09, 0.09, 0.00]   # não há mais "Em Trânsito"
    status.append(
        rng.choice(["Entregue", "Cancelado", "Devolvido", "Em Trânsito"], p=probs)
    )

# ----------------------------------------------------------------------------
# Sujeira proposital
# ----------------------------------------------------------------------------
# 1) Formatos de data misturados (50% YYYY-MM-DD, 50% DD/MM/YYYY)
mascara_fmt = rng.random(N_PEDIDOS) < 0.5
datas_str = np.where(
    mascara_fmt,
    datas.strftime("%Y-%m-%d"),
    datas.strftime("%d/%m/%Y"),
)

# 2) Variações de escrita nas categorias (minúsculas, MAIÚSCULAS, espaços extras)
cats_sujas = []
for c in cats:
    r = rng.random()
    if r < 0.78:
        cats_sujas.append(c)
    elif r < 0.88:
        cats_sujas.append(c.lower())
    elif r < 0.96:
        cats_sujas.append(c.upper())
    else:
        cats_sujas.append(f" {c} ")

# 3) ~5% de valor_frete nulo (exatamente 50 de 1.000)
fretes = fretes.astype(float)
n_nulos = int(round(N_PEDIDOS * PCT_FRETE_NO if False else N_PEDIDOS * PCT_FRETE_NULO))
idx_nulos = rng.choice(N_PEDIDOS, size=n_nulos, replace=False)
fretes[idx_nulos] = np.nan

# ----------------------------------------------------------------------------
# Montagem do DataFrame
# ----------------------------------------------------------------------------
df = pd.DataFrame({
    "id_pedido": ids,
    "data_pedido": datas_str,
    "uf_destino": ufs,
    "categoria_produto": cats_sujas,
    "valor_produto": valores,
    "valor_frete": fretes,
    "cupom_desconto": cupons,
    "status_pedido": status,
    "prazo_entrega_dias": prazos.astype(int),
})

# 4) 30 linhas duplicadas (cópias exatas), inseridas em posições aleatórias
df["_ordem"] = np.arange(len(df), dtype=float)
dups = df.sample(n=N_DUPLICADAS, random_state=SEED).copy()
dups["_ordem"] = dups["_ordem"] + rng.uniform(0.01, 0.99, size=N_DUPLICADAS)

df_final = (
    pd.concat([df, dups], ignore_index=True)
    .sort_values("_ordem", kind="stable")
    .drop(columns="_ordem")
    .reset_index(drop=True)
)

# ----------------------------------------------------------------------------
# Exportação
# ----------------------------------------------------------------------------
df_final.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8")

print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
print(f"Total de linhas: {len(df_final)} "
      f"({N_PEDIDOS} únicas + {N_DUPLICADAS} duplicadas)")
print(f"Duplicatas detectadas: {df_final.duplicated().sum()}")
print(f"Fretes nulos: {df_final['valor_frete'].isna().sum()}")
print(f"Período: {inicio} a {hoje}")
print(df_final.head(10).to_string(index=False))