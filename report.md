# Relatório de análise — Festa em Cena

A análise examinou 1.500 pedidos fictícios registrados entre agosto e novembro de 2024 e de 2025. Cada linha representa um pedido de um único produto, que pode conter várias unidades. O objetivo foi identificar problemas de qualidade antes de comparar canais e períodos, preservando o CSV original e evitando a criação de valores inexistentes.

Na limpeza de textos, 18 categorias vazias foram preenchidas com "sem categoria". Outras 1.482 categorias não vazias foram alteradas pela aplicação de remoção de espaços, conversão para letras minúsculas e retirada de pontuações com expressão regular. Os canais foram padronizados como Mercado, Loja física e Web. Todos os 1.500 registros tiveram o canal reconhecido, portanto nenhum pedido foi excluído dessa contagem.

A validação numérica encontrou sete pedidos com quantidade inválida e 12 com preço unitário ausente ou inválido. Como não houve sobreposição entre esses problemas, 19 pedidos distintos foram afetados. Os valores não foram substituídos por médias, zeros ou estimativas. Também foram encontradas quatro datas de venda inválidas. Elas foram marcadas e excluídas apenas da análise por período, permitindo que o restante do processamento continuasse.

A investigação da regra de negócio mostrou 143 pedidos sem data de entrega. Desses, 109 estavam cancelados e 34 possuíam outro status. Logo, a hipótese de que todo pedido sem entrega está cancelado é falsa. Entre os contraexemplos há pedidos com status Concluído e data de entrega ausente. Nenhum status foi modificado e nenhuma data foi inventada.

Na comparação entre canais, a Web apresentou 666 pedidos, seguida por Loja física, com 551, e Mercado, com 283. Assim, a Web concentrou o maior número de pedidos registrados na base. Esse resultado inclui todos os status e não representa receita, quantidade de unidades ou vendas concluídas.

Na análise temporal, outubro concentrou os maiores volumes nos dois anos: 393 pedidos em 2024-10 e 410 em 2025-10. O maior resultado foi 2025-10, com 410 pedidos. Isso sugere concentração próxima ao Halloween, celebrado em 31 de outubro. Entretanto, a base cobre somente agosto a novembro de dois anos, é fictícia e teve quatro datas inválidas excluídas.

A limpeza tornou as contagens mais confiáveis, mas não garante sozinha evitar overfitting ou underfitting em um futuro modelo. Representatividade dos dados, escolha do algoritmo e avaliação também seriam necessárias.