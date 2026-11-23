# 📊 Análise Operacional e Financeira de E-commerce

Projeto de análise de dados ponta a ponta desenvolvido para diagnosticar gargalos de faturamento, cancelamentos, desempenho logístico e eficácia de campanhas promocionais em uma operação de e-commerce.

---

## 🎯 Problema de Negócio
A operação precisava identificar onde estava perdendo receita, quais estados apresentavam os maiores gargalos de prazo e frete, qual o impacto real dos cupons de desconto no ticket médio e como o faturamento se comportava ao longo dos meses.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Python (Pandas):** Limpeza, padronização de texto, tratamento de datas e remoção de inconsistências (`vendas_ecommerce_limpo.csv`).
* **SQL (SQLite):** Modelagem relacional (`ecommerce.db`) e consultas analíticas para responder às perguntas de gestão (`analise-sql.py`).
* **OpenPyXL:** Automação de relatório executivo formatado em Excel (`relatorio_executivo_ecommerce.xlsx`) dividido por abas gerenciais.
* **Git & GitHub:** Versionamento de código e documentação.

---

## 🔍 Principais Descobertas (Insights)

1. **Concentração de Receita e Ralo de Cancelamentos:**
   * A categoria **Eletrônicos** lidera o faturamento real (**R$ 194.697,26** em 162 pedidos entregues), seguida por **Casa E Decoração** (**R$ 61.210,27**).
   * Por outro lado, **Eletrônicos** também concentra a maior perda financeira por cancelamentos (**R$ 25.867,75** em 26 pedidos) — mais de 5 vezes o valor perdido pela segunda colocada (**Casa E Decoração**, com **R$ 4.743,04**).
   * **Perfumaria** apresentou a maior estabilidade operacional, com apenas 9 pedidos cancelados (**R$ 2.442,14**).

2. **Desempenho Logístico e Sazonalidade:**
   * Mapeamento do frete médio e prazo de entrega por Unidade Federativa (UF) para identificar rotas críticas.
   * Análise da evolução mensal de faturamento (`STRFTIME`) para suporte ao planejamento de estoque.

3. **Eficácia de Cupons de Desconto:**
   * Comparação direta entre pedidos com e sem cupom, avaliando volume, taxa de conclusão e ticket médio.

---

## 💡 Recomendações de Negócio
* **Auditoria em Eletrônicos:** Investigar a causa raiz dos cancelamentos nessa categoria (ruptura de estoque, falha na aprovação de pagamento ou prazo de entrega) para recuperar até **R$ 25,8 mil** em receita.
* **Revisão de Malha Logística:** Renegociar transportadoras nos estados com maior prazo médio de entrega para reduzir desistências.

---

## 📁 Estrutura do Repositório
* `vendas_ecommerce_limpo.csv`: Base de dados tratada e padronizada.
* `ecommerce.db`: Banco de dados SQLite populado.
* `analise-sql.py`: Script com as 5 consultas SQL de negócio.
* `gerar-relatorio-excel.py`: Automação que exporta e estiliza o relatório executivo em `.xlsx`.
* `relatorio_executivo_ecommerce.xlsx`: Planilha final gerada automaticamente para a gestão.

---

*Desenvolvido por **Poliana Elizabeth** — Estudante de Análise e Desenvolvimento de Sistemas (ADS) | Dados, SQL & Automação.*