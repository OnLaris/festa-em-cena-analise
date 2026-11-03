import pandas as pd


def carregar_dados(caminho_arquivo):
    """Lê o CSV sem modificar o arquivo original."""

    dados = pd.read_csv(
        caminho_arquivo,
        sep=",",
        encoding="utf-8",
        dtype=str
    )

    return dados