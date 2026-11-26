from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from getpass import getpass

from mysql.connector import Error

import banco
from conexao import configurar, cursor_mysql


def escolher(titulo, opcoes, retorno="Voltar"):
    opcoes = tuple(opcoes)
    while True:
        print(f"=== {titulo} ===")
        for numero, opcao in enumerate(opcoes, 1):
            print(f"{numero}. {opcao}")
        print(f"0. {retorno}")
        escolha = input("> ").strip()
        if escolha == "0":
            return None
        if escolha in {str(numero) for numero in range(1, len(opcoes) + 1)}:
            return opcoes[int(escolha) - 1]
        print("Opção inválida.")


def ler_valor(campo, tipo):
    opcional = tipo.endswith("?")
    tipo = tipo.rstrip("?")
    formato = {"data": "AAAA-MM-DD", "data_hora": "AAAA-MM-DD HH:MM:SS",
               "valor": "ex.: 29,90", "id": "inteiro positivo"}.get(tipo)
    detalhes = [parte for parte in (formato, "Enter para NULL" if opcional else None) if parte]
    rotulo = f"{campo} ({', '.join(detalhes)}): " if detalhes else f"{campo}: "

    while True:
        entrada = (getpass(rotulo) if tipo == "senha" else input(rotulo)).strip()
        if not entrada:
            if opcional:
                return None
            print("Campo obrigatório.")
            continue
        try:
            if tipo == "id":
                valor = int(entrada)
                if 0 < valor <= 2_147_483_647:
                    return valor
                raise ValueError
            if tipo == "data":
                return date.fromisoformat(entrada)
            if tipo == "data_hora":
                return datetime.strptime(entrada, "%Y-%m-%d %H:%M:%S")
            if tipo == "valor":
                valor = Decimal(entrada.replace(",", "."))
                if valor.is_finite() and 0 <= valor <= Decimal("99999999.99") and valor == round(valor, 2):
                    return valor
                raise ValueError
            return entrada
        except (ValueError, InvalidOperation):
            print(f"Valor inválido. Formato esperado: {formato}.")


def exibir(registros):
    if not registros:
        print("Nenhum registro encontrado.")
        return

    for registro in registros:
        print(" | ".join(f"{campo}: {valor if valor is not None else 'NULL'}"
                         for campo, valor in registro.items()))
    print(f"Total: {len(registros)} registro(s).")


def ler_filtro(tabela):
    campos = banco.campos_busca(tabela)
    campo = escolher("Atributo do filtro (texto aceita parte do valor)", campos)
    return {campo: ler_valor(campo, campos[campo])} if campo else None


def cadastrar(config, tabela):
    if tabela == "compra":
        usuario = ler_valor("id_usuario", "id")
        jogo = ler_valor("id_jogo", "id")
        pagamento = ler_valor("forma_pagamento", "texto?")
        print(banco.registrar_compra(config, usuario, jogo, pagamento))
        return

    _, campos = banco.ENTIDADES[tabela]
    dados = {campo: ler_valor(campo, tipo) for campo, tipo in campos.items()}
    novo_id = banco.cadastrar(config, tabela, dados)
    print(f"Registro cadastrado com ID {novo_id}.")


def atualizar(config, tabela):
    _, campos = banco.ENTIDADES[tabela]
    campo = escolher("Atributo a atualizar", campos)
    if campo is None:
        return
    escopo = escolher("Escopo da atualização", ("Com filtro", "Todos os registros"))
    if escopo is None:
        return
    filtros = ler_filtro(tabela) if escopo == "Com filtro" else {}
    if filtros is None:
        return
    valor = ler_valor(campo, campos[campo])
    if not filtros and input(f"Digite TODOS para alterar {campo} em toda a tabela {tabela}: ") != "TODOS":
        print("Atualização cancelada.")
        return
    quantidade = banco.atualizar(config, tabela, campo, valor, filtros)
    print(f"{quantidade} registro(s) alterado(s).")


def remover(config, tabela):
    chaves, _ = banco.ENTIDADES[tabela]
    filtros = {chave: ler_valor(chave, "id") for chave in chaves}
    registros = banco.listar(config, tabela, filtros)
    exibir(registros)
    if not registros:
        return
    if tabela == "usuario":
        print("A exclusão também remove o perfil e as compras vinculadas.")
    if input("Digite SIM para confirmar a remoção: ") != "SIM":
        print("Remoção cancelada.")
        return
    quantidade = banco.remover(config, tabela, filtros)
    print(f"{quantidade} registro(s) removido(s) da tabela {tabela}.")


def buscar(config, tabela):
    filtros = ler_filtro(tabela)
    if filtros is not None:
        exibir(banco.listar(config, tabela, filtros))


def menu_entidade(config, tabela):
    operacoes = {
        "Listar todos": lambda: exibir(banco.listar(config, tabela, {})),
        "Buscar por filtro": lambda: buscar(config, tabela),
        "Cadastrar": lambda: cadastrar(config, tabela),
        "Atualizar": lambda: atualizar(config, tabela),
        "Remover pela chave primária": lambda: remover(config, tabela),
    }
    while opcao := escolher(tabela.capitalize(), operacoes):
        try:
            operacoes[opcao]()
        except Error as erro:
            print(f"Operação não concluída: {erro.msg}")


def main():
    try:
        config = configurar()
        with cursor_mysql(config):
            print("Conectado ao banco STEAM_DB.")
    except (Error, ValueError) as erro:
        print(f"Não foi possível conectar ao MySQL: {erro}")
        return 1

    consultas = "Consultas com JOIN"
    while opcao := escolher("Plataforma de Jogos Digitais", (*banco.ENTIDADES, consultas), "Sair"):
        if opcao != consultas:
            menu_entidade(config, opcao)
            continue
        while consulta := escolher(consultas, banco.JOINS):
            try:
                exibir(banco.consultar(config, banco.JOINS[consulta]))
            except Error as erro:
                print(f"Consulta não concluída: {erro.msg}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EOFError, KeyboardInterrupt):
        print("Sessão encerrada.")
