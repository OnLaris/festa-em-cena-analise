import re
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


def texto_ausente(valor):
    """Verifica se um valor está nulo ou contém apenas espaços."""

    if pd.isna(valor):
        return True

    return str(valor).strip() == ""


def limpar_categoria(valor):
    """Padroniza uma categoria e preenche valores vazios."""

    # Categoria nula ou contendo apenas espaços.
    if texto_ausente(valor):
        return "sem categoria"

    # Remove espaços nas pontas e transforma em minúsculas.
    texto = str(valor).strip().lower()

    texto = re.sub(r"[^a-z\s]", "", texto)

    texto = re.sub(r"\s+", " ", texto).strip()

    if texto == "":
        return "sem categoria"

    return texto


def tratar_categorias(dados):
    """
    Limpa a coluna categoria e retorna:
    - o DataFrame tratado;
    - o total de categorias vazias preenchidas;
    - o total de categorias não vazias alteradas.
    """

    dados = dados.copy()

    # Preserva os textos originais para comparação.
    dados["categoria_original"] = dados["categoria"]

    # Identifica as categorias que estavam originalmente vazias.
    categorias_vazias = dados["categoria_original"].apply(
        texto_ausente
    )

    # Aplica a função de limpeza em todas as categorias.
    dados["categoria"] = dados["categoria_original"].apply(
        limpar_categoria
    )

    # Identifica categorias não vazias que foram modificadas.
    categorias_alteradas = (
        (~categorias_vazias)
        & (
            dados["categoria_original"].astype(str)
            != dados["categoria"]
        )
    )

    total_vazias = int(categorias_vazias.sum())
    total_alteradas = int(categorias_alteradas.sum())

    return dados, total_vazias, total_alteradas