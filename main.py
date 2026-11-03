from funcoes import (
    analisar_entrega_status,
    carregar_dados,
    contar_pedidos_por_canal,
    contar_pedidos_por_periodo,
    tratar_canais,
    tratar_categorias,
    tratar_datas_venda,
    validar_valores_numericos
)


def main():
    dados = carregar_dados("halloween_vendas.csv")

    print("Total de linhas:", len(dados))

    print("\nTrês primeiros registros:")
    print(dados.head(3))

    print("\nColunas encontradas:")
    print(dados.columns.tolist())

    print("\nValores ausentes por coluna:")
    print(dados.isna().sum())

    dados, total_vazias, total_alteradas = tratar_categorias(
        dados
    )

    print("\nTratamento das categorias")
    print(
        "Categorias vazias preenchidas:",
        total_vazias
    )
    print(
        "Categorias não vazias alteradas:",
        total_alteradas
    )

    categoria_original_comparacao = (
        dados["categoria_original"]
        .fillna("")
        .astype(str)
    )

    exemplos_categorias = dados[
        categoria_original_comparacao
        != dados["categoria"]
    ][
        ["categoria_original", "categoria"]
    ].head(10)

    print("\nExemplos de categorias tratadas:")
    print(exemplos_categorias)

    (
        dados,
        total_canais_reconhecidos,
        total_canais_nao_reconhecidos
    ) = tratar_canais(dados)

    print("\nTratamento dos canais de venda")
    print(
        "Canais reconhecidos:",
        total_canais_reconhecidos
    )
    print(
        "Canais não reconhecidos:",
        total_canais_nao_reconhecidos
    )


    (
        dados,
        total_problemas_quantidade,
        total_problemas_preco,
        total_pedidos_afetados
    ) = validar_valores_numericos(dados)

    print("\nValidação de quantidade e preço")
    print(
        "Problemas na quantidade:",
        total_problemas_quantidade
    )
    print(
        "Problemas no preço unitário:",
        total_problemas_preco
    )
    print(
        "Pedidos afetados por algum problema numérico:",
        total_pedidos_afetados
    )

    exemplos_problemas = dados[
        dados["problema_numerico"]
    ][
        [
            "pedido_id",
            "quantidade",
            "preco_unitario",
            "problema_quantidade",
            "problema_preco"
        ]
    ].head(10)

    print("\nExemplos de problemas numéricos:")
    print(exemplos_problemas)

    (
        dados,
        resultado_entrega,
        exemplos_contraexemplos
    ) = analisar_entrega_status(dados)

    print("\nRegra de pedidos sem data de entrega")

    print(
        "Total de pedidos cancelados:",
        resultado_entrega["total_cancelados"]
    )

    print(
        "Sem entrega e cancelados:",
        resultado_entrega[
            "sem_entrega_cancelados"
        ]
    )

    print(
        "Sem entrega e com outro status:",
        resultado_entrega[
            "sem_entrega_outro_status"
        ]
    )

    if resultado_entrega["hipotese_verdadeira"]:
        print(
            "Conclusão: a hipótese é verdadeira na base."
        )
    else:
        print(
            "Conclusão: a hipótese é falsa na base."
        )

        print("\nAté três contraexemplos:")
        print(exemplos_contraexemplos)
        dados, total_datas_invalidas = tratar_datas_venda(
        dados
    )

    print("\nTratamento das datas de venda")
    print(
        "Datas de venda inválidas ou vazias:",
        total_datas_invalidas
    )

    print("\nExemplos de datas convertidas:")
    print(
        dados[
            [
                "data_venda_original",
                "data_venda_brasileira",
                "ano",
                "mes",
                "dia",
                "hora",
                "ano_mes"
            ]
        ].head(5)
    )

    exemplos_datas_invalidas = dados.loc[
        ~dados["data_venda_valida"],
        [
            "pedido_id",
            "data_venda_original"
        ]
    ].head(5)

    if exemplos_datas_invalidas.empty:
        print("\nNenhuma data de venda inválida.")
    else:
        print("\nExemplos de datas de venda inválidas:")
        print(exemplos_datas_invalidas)

    (
        contagem_canais,
        canais_excluidos
    ) = contar_pedidos_por_canal(dados)

    print("\nPedidos registrados por canal:")
    print(contagem_canais)

    print(
        "Registros excluídos da contagem por canal:",
        canais_excluidos
    )

    (
        contagem_periodos,
        datas_excluidas
    ) = contar_pedidos_por_periodo(dados)

    print("\nPedidos registrados por ano-mês:")
    print(contagem_periodos)

    print(
        "Registros excluídos da contagem por período:",
        datas_excluidas
    )

    if not contagem_canais.empty:
        canal_destaque = contagem_canais.idxmax()
        pedidos_canal_destaque = int(
            contagem_canais.max()
        )

        print("\nDescoberta por canal:")
        print(
            f"{canal_destaque} apresentou "
            f"{pedidos_canal_destaque} pedidos registrados."
        )
        print(
            "Interpretação: foi o canal com maior número "
            "de pedidos na base analisada."
        )
        print(
            "Limitação: a contagem inclui todos os status "
            "e não representa receita ou vendas concluídas."
        )

    if not contagem_periodos.empty:
        periodo_destaque = contagem_periodos.idxmax()
        pedidos_periodo_destaque = int(
            contagem_periodos.max()
        )

        print("\nDescoberta por período:")
        print(
            f"{periodo_destaque} apresentou "
            f"{pedidos_periodo_destaque} pedidos registrados."
        )
        print(
            "Interpretação: foi o período com maior número "
            "de pedidos entre os períodos analisados."
        )
        print(
            "Limitação: o resultado considera apenas datas "
            "válidas da base fictícia."
        )

        print("\n" + "=" * 60)
        print("RELATÓRIO FINAL — FESTA EM CENA")
        print("=" * 60)

        print("\n1. VISÃO GERAL")
        print("Total de linhas lidas:", len(dados))

        print("\n2. TRATAMENTO DAS CATEGORIAS")
        print(
            "Categorias vazias preenchidas:",
            total_vazias
        )
        print(
            "Categorias não vazias alteradas:",
            total_alteradas
        )

        print("\n3. VALIDAÇÃO NUMÉRICA")
        print(
            "Problemas na quantidade:",
            total_problemas_quantidade
        )
        print(
            "Problemas no preço unitário:",
            total_problemas_preco
        )
        print(
            "Pedidos com algum problema numérico:",
            total_pedidos_afetados
        )

        print("\n4. VALIDAÇÃO DAS DATAS")
        print(
            "Datas de venda inválidas ou vazias:",
            total_datas_invalidas
        )

        print("\n5. STATUS E DATA DE ENTREGA")
        print(
            "Total de pedidos cancelados:",
            resultado_entrega["total_cancelados"]
        )
        print(
            "Sem entrega e cancelados:",
            resultado_entrega[
                "sem_entrega_cancelados"
            ]
        )
        print(
            "Sem entrega e com outro status:",
            resultado_entrega[
                "sem_entrega_outro_status"
            ]
        )

        if resultado_entrega["hipotese_verdadeira"]:
            print(
                "Conclusão: a hipótese é verdadeira."
            )
        else:
            print(
                "Conclusão: a hipótese é falsa."
            )

        print("\n6. PEDIDOS REGISTRADOS POR CANAL")

        for canal, quantidade in contagem_canais.items():
            print(
                f"{canal}: {int(quantidade)} pedidos"
            )

        print(
            "Registros excluídos por canal:",
            canais_excluidos
        )

        print("\n7. PEDIDOS REGISTRADOS POR ANO-MÊS")

        for periodo, quantidade in contagem_periodos.items():
            print(
                f"{periodo}: {int(quantidade)} pedidos"
            )

        print(
            "Registros excluídos por data:",
            datas_excluidas
        )

        print("\n8. OBSERVAÇÃO")
        print(
            "As contagens representam pedidos registrados, "
            "não unidades, receita ou vendas concluídas."
        )

        print("=" * 60)

if __name__ == "__main__":
    main()