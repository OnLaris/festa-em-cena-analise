# Análise de pedidos da Festa em Cena

## Descrição do projeto

Este projeto analisa uma base fictícia da Festa em Cena, uma rede que vende fantasias e acessórios de Halloween pelos canais Mercado, Loja física e Web.

A base contém 1.500 pedidos registrados entre agosto e novembro de 2024 e de 2025. Antes de comparar canais e períodos, o programa verifica problemas em categorias, canais, quantidades, preços e datas.

O CSV original é preservado. Os valores problemáticos são marcados, mas não são substituídos por informações inventadas.

## Objetivo

O objetivo é aplicar lógica de programação, Pandas, funções, condicionais, laços, dicionários, expressões regulares e `datetime` para:

- ler e inspecionar o CSV;
- limpar e padronizar textos;
- validar quantidade e preço unitário;
- identificar datas de venda inválidas;
- investigar pedidos sem data de entrega;
- contar pedidos por canal e por ano-mês;
- produzir descobertas com evidências numéricas e limitações.

## Significado dos dados

Cada linha representa um pedido de um único produto. Um pedido pode possuir mais de uma unidade, por isso quantidade de pedidos e quantidade de unidades não são a mesma medida.

Algumas colunas importantes:

- `pedido_id`: identificador do pedido.
- `data_venda`: data e horário em que o pedido foi registrado.
- `categoria`: categoria do produto vendido.
- `canal_venda`: canal pelo qual o pedido foi realizado.
- `quantidade`: número de unidades do produto no pedido.
- `preco_unitario`: preço de uma unidade do produto.
- `status_pedido`: situação registrada para o pedido.
- `data_entrega`: data e horário registrados para a entrega.

As colunas de custo e desconto estão presentes no CSV, mas não foram necessárias para as análises obrigatórias.

## Estrutura do projeto

```text
festa-em-cena/
├── main.py
├── funcoes.py
├── halloween_vendas.csv
├── README.md
├── report.md
├── requirements.txt
└── .gitignore