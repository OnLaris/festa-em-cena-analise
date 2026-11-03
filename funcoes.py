import re

import pandas as pd


MAPA_CANAIS = {
    "mercado": "Mercado",
    "loja fisica": "Loja física",
    "loja física": "Loja física",
    "web": "Web",
}


def carregar_dados(caminho_arquivo):
    """Lê o CSV como texto sem modificar o arquivo original."""

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
    """
    Padroniza uma categoria com strip, lower e re.sub.
    Valores vazios são preenchidos com 'sem categoria'.
    """

    if texto_ausente(valor):
        return "sem categoria"

    texto = str(valor).strip().lower()
    texto = re.sub(r"[^a-z\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    if texto == "":
        return "sem categoria"

    return texto


def tratar_categorias(dados):
    """
    Preserva a categoria original, aplica a limpeza e retorna
    as contagens de categorias vazias e não vazias alteradas.
    """

    dados = dados.copy()
    dados["categoria_original"] = dados["categoria"]

    categorias_vazias = dados["categoria_original"].apply(
        texto_ausente
    )

    dados["categoria"] = dados["categoria_original"].apply(
        limpar_categoria
    )

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


def padronizar_canal(valor):
    """
    Padroniza o canal como Mercado, Loja física ou Web.
    Valores não reconhecidos retornam None.
    """

    if texto_ausente(valor):
        return None

    canal_normalizado = str(valor).strip().lower()

    return MAPA_CANAIS.get(canal_normalizado)


def tratar_canais(dados):
    """
    Preserva o canal original, aplica a padronização e retorna
    as contagens de canais reconhecidos e não reconhecidos.
    """

    dados = dados.copy()
    dados["canal_venda_original"] = dados["canal_venda"]

    dados["canal_venda"] = dados[
        "canal_venda_original"
    ].apply(padronizar_canal)

    canais_reconhecidos = dados["canal_venda"].notna()
    canais_nao_reconhecidos = dados["canal_venda"].isna()

    total_canais_reconhecidos = int(
        canais_reconhecidos.sum()
    )

    total_canais_nao_reconhecidos = int(
        canais_nao_reconhecidos.sum()
    )

    return (
        dados,
        total_canais_reconhecidos,
        total_canais_nao_reconhecidos
    )


def validar_valores_numericos(dados):
    """
    Valida quantidade e preço sem inventar valores.
    Retorna o DataFrame e as contagens de problemas.
    """

    dados = dados.copy()

    quantidade_numerica = pd.to_numeric(
        dados["quantidade"],
        errors="coerce"
    )

    preco_numerico = pd.to_numeric(
        dados["preco_unitario"],
        errors="coerce"
    )

    quantidade_valida = (
        quantidade_numerica.notna()
        & (quantidade_numerica > 0)
        & (quantidade_numerica % 1 == 0)
    )

    preco_valido = (
        preco_numerico.notna()
        & (preco_numerico >= 0)
    )

    dados["quantidade_convertida"] = quantidade_numerica
    dados["preco_unitario_convertido"] = preco_numerico

    dados["problema_quantidade"] = ~quantidade_valida
    dados["problema_preco"] = ~preco_valido

    dados["problema_numerico"] = (
        dados["problema_quantidade"]
        | dados["problema_preco"]
    )

    total_problemas_quantidade = int(
        dados["problema_quantidade"].sum()
    )

    total_problemas_preco = int(
        dados["problema_preco"].sum()
    )

    total_pedidos_afetados = int(
        dados["problema_numerico"].sum()
    )

    return (
        dados,
        total_problemas_quantidade,
        total_problemas_preco,
        total_pedidos_afetados
    )