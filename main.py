from funcoes import carregar_dados, tratar_categorias


def main():
    dados = carregar_dados("halloween_vendas.csv")

    print("Total de linhas:", len(dados))

    print("\nTrês primeiros registros:")
    print(dados.head(3))

    print("\nColunas encontradas:")
    print(dados.columns.tolist())

    print("\nValores ausentes por coluna:")
    print(dados.isna().sum())

    # Esta linha cria as variáveis usadas abaixo.
    dados, total_vazias, total_alteradas = tratar_categorias(
        dados
    )

    print("\nTratamento das categorias")
    print("Categorias vazias preenchidas:", total_vazias)
    print(
        "Categorias não vazias alteradas:",
        total_alteradas
    )

    exemplos_alterados = dados[
        dados["categoria_original"].fillna("").astype(str)
        != dados["categoria"]
    ][
        ["categoria_original", "categoria"]
    ].head(10)

    print("\nExemplos de categorias tratadas:")
    print(exemplos_alterados)


if __name__ == "__main__":
    main()