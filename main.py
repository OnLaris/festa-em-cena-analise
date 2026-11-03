from funcoes import carregar_dados


def main():
    dados = carregar_dados("halloween_vendas.csv")

    print("Total de linhas:", len(dados))
    print("\nTrês primeiros registros:")
    print(dados.head(3))

    print("\nColunas encontradas:")
    print(dados.columns.tolist())

    print("\nValores ausentes por coluna:")
    print(dados.isna().sum())


if __name__ == "__main__":
    main()