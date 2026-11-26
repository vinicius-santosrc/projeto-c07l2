
import usuario_dao
import perfil_dao
import desenvolvedora_dao
import categoria_dao
import jogo_dao
import compra_dao
import consulta_dao


def ler_valor(campo, tipo):
    valor = input(campo + ": ")

    if valor == "" and "?" in tipo:
        return None

    if tipo == "id":
        return int(valor)

    if tipo == "valor":
        return float(valor.replace(",", "."))

    return valor


def mostrar(registros):
    for registro in registros:
        print(registro)

    print("Total de registros:", len(registros))


def inserir(dao):
    if dao == compra_dao:
        id_usuario = int(input("ID do usuario: "))
        id_jogo = int(input("ID do jogo: "))
        pagamento = input("Forma de pagamento: ")

        resultado = dao.inserir(id_usuario, id_jogo, pagamento)
        print(resultado)

    else:
        dados = {}

        for campo in dao.CAMPOS:
            dados[campo] = ler_valor(campo, dao.CAMPOS[campo])

        resultado = dao.inserir(**dados)

        if resultado:
            print("Registro cadastrado com sucesso!")


def buscar(dao):
    print("Campos disponiveis:")

    for campo in dao.CHAVE:
        print(campo)

    for campo in dao.CAMPOS:
        if campo != "senha":
            print(campo)

    campo = input("Digite o campo que deseja buscar: ")

    if campo in dao.CHAVE:
        valor = int(input("Digite o ID: "))

    elif campo in dao.CAMPOS and campo != "senha":
        valor = ler_valor(campo, dao.CAMPOS[campo])

    else:
        print("Campo invalido")
        return

    registros = dao.buscar(campo, valor)
    mostrar(registros)


def atualizar(dao):
    print("Campos disponiveis para atualizar:")

    for campo in dao.CAMPOS:
        print(campo)

    campo = input("Qual campo deseja atualizar? ")

    if campo not in dao.CAMPOS:
        print("Campo invalido")
        return

    novo_valor = ler_valor(campo, dao.CAMPOS[campo])

    print("1 - Atualizar com filtro")
    print("2 - Atualizar todos")

    opcao = input("Escolha: ")

    if opcao == "1":
        print("Campos para filtro:")

        for chave in dao.CHAVE:
            print(chave)

        for atributo in dao.CAMPOS:
            if atributo != "senha":
                print(atributo)

        filtro = input("Campo do filtro: ")

        if filtro in dao.CHAVE:
            valor = int(input("Digite o ID: "))

        elif filtro in dao.CAMPOS and filtro != "senha":
            valor = ler_valor(filtro, dao.CAMPOS[filtro])

        else:
            print("Campo invalido")
            return

        total = dao.atualizar(campo, novo_valor, filtro, valor)
        print("Registros atualizados:", total)

    elif opcao == "2":
        confirmar = input("Deseja atualizar todos? (s/n): ")

        if confirmar == "s":
            total = dao.atualizar(campo, novo_valor)
            print("Registros atualizados:", total)

    else:
        print("Opcao invalida")


def remover(dao):
    ids = []

    for campo in dao.CHAVE:
        valor = int(input(campo + ": "))
        ids.append(valor)

    confirmar = input("Deseja remover o registro? (s/n): ")

    if confirmar == "s":
        total = dao.remover(*ids)
        print("Registros removidos:", total)


def menu_entidade(dao):
    while True:
        print("===== " + dao.TABELA + " =====")
        print("1 - Listar todos")
        print("2 - Buscar")
        print("3 - Inserir")
        print("4 - Atualizar")
        print("5 - Remover")
        print("0 - Voltar")

        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == "1":
                mostrar(dao.listar())

            elif opcao == "2":
                buscar(dao)

            elif opcao == "3":
                inserir(dao)

            elif opcao == "4":
                atualizar(dao)

            elif opcao == "5":
                remover(dao)

            elif opcao == "0":
                break

            else:
                print("Opcao invalida")

        except ValueError:
            print("Valor digitado invalido")


def menu_consultas():
    while True:
        print("===== CONSULTAS =====")
        print("1 - Usuarios e perfis (1:1)")
        print("2 - Desenvolvedoras e jogos (1:N)")
        print("3 - Usuarios e jogos comprados (N:M)")
        print("0 - Voltar")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            mostrar(consulta_dao.consulta_1())

        elif opcao == "2":
            mostrar(consulta_dao.consulta_2())

        elif opcao == "3":
            mostrar(consulta_dao.consulta_3())

        elif opcao == "0":
            break

        else:
            print("Opcao invalida")


def main():
    while True:
        print("===== PLATAFORMA DE JOGOS =====")
        print("1 - Usuarios")
        print("2 - Perfis")
        print("3 - Desenvolvedoras")
        print("4 - Categorias")
        print("5 - Jogos")
        print("6 - Compras")
        print("7 - Consultas com JOIN")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            menu_entidade(usuario_dao)

        elif opcao == "2":
            menu_entidade(perfil_dao)

        elif opcao == "3":
            menu_entidade(desenvolvedora_dao)

        elif opcao == "4":
            menu_entidade(categoria_dao)

        elif opcao == "5":
            menu_entidade(jogo_dao)

        elif opcao == "6":
            menu_entidade(compra_dao)

        elif opcao == "7":
            menu_consultas()

        elif opcao == "0":
            print("Encerrando programa...")
            break

        else:
            print("Opcao invalida")


if __name__ == "__main__":
    main()
