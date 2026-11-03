import re
from datetime import datetime

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


def analisar_entrega_status(dados):
    """
    Investiga se todos os pedidos sem data de entrega
    possuem o status Cancelado.
    """

    dados = dados.copy()

    status_comparacao = (
        dados["status_pedido"]
        .fillna("")
        .str.strip()
        .str.lower()
    )

    entrega_comparacao = (
        dados["data_entrega"]
        .fillna("")
        .str.strip()
    )

    sem_data_entrega = entrega_comparacao == ""
    status_cancelado = status_comparacao == "cancelado"

    sem_entrega_cancelado = (
        sem_data_entrega
        & status_cancelado
    )

    sem_entrega_outro_status = (
        sem_data_entrega
        & (~status_cancelado)
    )

    dados["sem_data_entrega"] = sem_data_entrega

    total_cancelados = int(
        status_cancelado.sum()
    )

    total_sem_entrega_cancelados = int(
        sem_entrega_cancelado.sum()
    )

    total_sem_entrega_outro_status = int(
        sem_entrega_outro_status.sum()
    )

    hipotese_verdadeira = (
        total_sem_entrega_outro_status == 0
    )

    exemplos_contraexemplos = dados.loc[
        sem_entrega_outro_status,
        [
            "pedido_id",
            "data_entrega",
            "status_pedido"
        ]
    ].head(3)

    resultado = {
        "total_cancelados": total_cancelados,
        "sem_entrega_cancelados": (
            total_sem_entrega_cancelados
        ),
        "sem_entrega_outro_status": (
            total_sem_entrega_outro_status
        ),
        "hipotese_verdadeira": hipotese_verdadeira
    }

    return dados, resultado, exemplos_contraexemplos

def converter_data_venda(valor):
    """
    Converte uma data no formato ano-mês-dia hora:minuto:segundo.
    Retorna None quando o texto está vazio ou é inválido.
    """

    if texto_ausente(valor):
        return None

    try:
        return datetime.strptime(
            str(valor).strip(),
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None


def tratar_datas_venda(dados):
    """
    Preserva a data original, converte as datas e cria
    colunas com ano, mês, dia, hora e formato brasileiro.
    """

    dados = dados.copy()
    dados["data_venda_original"] = dados["data_venda"]

    datas_convertidas = []
    anos = []
    meses = []
    dias = []
    horas = []
    datas_brasileiras = []
    periodos = []

    for valor in dados["data_venda_original"]:
        data_convertida = converter_data_venda(valor)
        datas_convertidas.append(data_convertida)

        if data_convertida is None:
            anos.append(None)
            meses.append(None)
            dias.append(None)
            horas.append(None)
            datas_brasileiras.append(None)
            periodos.append(None)
        else:
            anos.append(data_convertida.year)
            meses.append(data_convertida.month)
            dias.append(data_convertida.day)
            horas.append(data_convertida.hour)
            datas_brasileiras.append(
                data_convertida.strftime("%d/%m/%Y")
            )
            periodos.append(
                data_convertida.strftime("%Y-%m")
            )

    dados["data_venda_convertida"] = datas_convertidas
    dados["data_venda_valida"] = dados[
        "data_venda_convertida"
    ].notna()

    dados["ano"] = pd.array(anos, dtype="Int64")
    dados["mes"] = pd.array(meses, dtype="Int64")
    dados["dia"] = pd.array(dias, dtype="Int64")
    dados["hora"] = pd.array(horas, dtype="Int64")
    dados["data_venda_brasileira"] = datas_brasileiras
    dados["ano_mes"] = periodos

    total_datas_invalidas = int(
        (~dados["data_venda_valida"]).sum()
    )

    return dados, total_datas_invalidas


def contar_pedidos_por_canal(dados):
    """
    Conta pedidos por canal usando somente canais reconhecidos.
    Todos os status são incluídos.
    """

    canais_reconhecidos = dados["canal_venda"].notna()

    contagem_canais = (
        dados.loc[canais_reconhecidos]
        .groupby("canal_venda")
        .size()
        .sort_values(ascending=False)
    )

    total_excluidos = int(
        (~canais_reconhecidos).sum()
    )

    return contagem_canais, total_excluidos


def contar_pedidos_por_periodo(dados):
    """
    Conta pedidos por ano-mês usando somente datas válidas.
    Todos os status são incluídos.
    """

    datas_validas = (
        dados["data_venda_valida"]
        & dados["ano_mes"].notna()
    )

    contagem_periodos = (
        dados.loc[datas_validas]
        .groupby("ano_mes")
        .size()
        .sort_index()
    )

    total_excluidos = int(
        (~datas_validas).sum()
    )

    return contagem_periodos, total_excluidos