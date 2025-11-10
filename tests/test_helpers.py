import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import (
    allowed_file,
    detectar_tipos_documento,
    normalizar_numero_conta,
    extrair_numero_conta_multiplos_metodos,
    verificar_periodo_completo,
)


def test_allowed_file_accepts_pdf_case_insensitive():
    assert allowed_file("documento.PDF")
    assert not allowed_file("documento.txt")


def test_detectar_tipos_documento_identifica_multiplos_tipos():
    texto = (
        "Relatório de Conciliação Bancária e extrato de Conta Corrente, com "
        "detalhes da Poupança e Aplicação em investimento."
    )
    tipos = detectar_tipos_documento(texto)
    assert tipos == [
        "Conciliação Bancária",
        "Conta Corrente",
        "Conta Poupança",
        "Conta de Aplicação",
    ]


def test_detectar_tipos_documento_padrao_corrente_quando_nao_identifica():
    assert detectar_tipos_documento("texto sem palavras-chave") == [
        "Conta Corrente"
    ]


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("00170.010-3", "1700103"),
        ("015.623-X", "15623X"),
        ("000000123", "123"),
    ],
)
def test_normalizar_numero_conta_remove_formatacao(entrada, esperado):
    assert normalizar_numero_conta(entrada) == esperado


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("CONTA: 8.304-6\nNúmero alternativo 0000083046", "8.304-6"),
        ("Dados bancários\nConta corrente 00012345", "00012345"),
    ],
)
def test_extrair_numero_conta_multiplos_metodos_prioriza_formatado(texto, esperado):
    assert extrair_numero_conta_multiplos_metodos(texto) == esperado


@pytest.mark.parametrize(
    "data_inicio, data_fim, mes, ano, esperado",
    [
        ("01/01/2024", "31/01/2024", "01", 2024, True),
        ("01/01/2024", "31/01/2024", "01", "2024", True),
        ("02/01/2024", "31/01/2024", "01", 2024, False),
        ("01/02/2024", "29/02/2024", "01", 2024, False),
        ("01/02/2024", "28/02/2023", "02", 2023, False),
    ],
)
def test_verificar_periodo_completo(data_inicio, data_fim, mes, ano, esperado):
    assert verificar_periodo_completo(data_inicio, data_fim, mes, ano) is esperado
