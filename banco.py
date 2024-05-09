import builtins
import datetime
import hashlib
import random
import string
import textwrap


class Cliente:
    def __init__(self, nome: str, cpf: str, data_nascimento: datetime.date, senha: str):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.senha_hash = self.gerar_senha_hash(senha)

    def gerar_senha_hash(self, senha: str) -> str:
        senha_salgada = senha + self.cpf
        return hashlib.sha256(senha_salgada.encode("utf-8")).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        senha_hash = self.gerar_senha_hash(senha)
        return senha_hash == self.senha_hash


class Conta:
    def __init__(self, cliente: Cliente, numero: int, saldo: float, limite: float):
        self.cliente = cliente
        self.numero = numero
        self.saldo = saldo
        self.limite = limite


def buscar_conta(numero_conta: int, contas: list) -> Conta:
    for conta in contas:
        if conta.numero == numero_conta:
            return conta
    return None


def verifica_saldo(valor: float, conta: Conta) -> bool:
    return conta.saldo >= valor


def verifica_limite_saque(valor: float, conta: Conta) -> bool:
    return valor <= conta.limite


def atualiza_extrato(conta: Conta, acao: str, valor: float):
    global extrato
    extrato += f"{conta.numero} {acao}: R$ {valor:.2f}\n"


def depositar(conta: Conta, valor: float):
    if valor > 0:
        conta.saldo += valor
        atualiza_extrato(conta, "Depósito", valor)
        print(f"Depósito realizado com sucesso! Saldo atual: R$ {conta.saldo:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")


def sacar(conta: Conta, valor: float):
    if not verifica_saldo(valor, conta):
        print("Operação falhou! Saldo insuficiente.")
    elif verifica_limite_saque(valor, conta) and valor > 0:
        conta.saldo -= valor
        conta.limite += valor
        atualiza_extrato(conta, "Saque", valor)
        print(f"Saque realizado com sucesso! Saldo atual: R$ {conta.saldo:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")


def transferir(conta_origem: Conta, conta_destino: Conta, valor: float):
    if not verifica_saldo(valor, conta_origem):
        print("Operação falhou! Saldo insuficiente na conta de origem.")
    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        conta_origem.saldo -= valor
        conta_destino.saldo += valor
        atualiza_extrato(conta_origem, "Transferência (enviada)", valor)
        atualiza_extrato(conta_destino, "Transferência (recebida)", valor)
        print(f"Transferência realizada com sucesso! Saldo atual: R$ {conta_origem.saldo:.2f}")


def pagar_conta(conta: Conta, codigo_conta: str, valor: float):
    if not verifica_saldo(valor, conta):
        print("Operação falhou! Saldo insuficiente.")
    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        conta.saldo -= valor
        atualiza_extrato(conta, "Pagamento de conta", valor)
        print(f"Pagamento de conta realizado com sucesso! Saldo atual: R$ {conta.saldo:.2f}")

def criar_conta(cliente: Cliente, numero: int, contas: list) -> Conta:
    if buscar_conta(numero, contas):
        print("Operação falhou! Já existe uma conta com este número.")
        return None

    nova_conta = Conta(cliente, numero, 0, 500)
    contas.append(nova_conta)
    print(f"Conta criada com sucesso! Número da conta: {nova_conta.numero}")
    return nova_conta


def gerar_senha_aleatoria() -> str:
    tamanho = 8
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(caracteres) for i in range(tamanho))


def criar_usuario(usuarios: list):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = datetime.datetime.strptime(
        builtins.input("Informe a data de nascimento (YYYY-MM-DD): "), "%Y-%m-%d"
    ).date()
    senha = gerar_senha_aleatoria()

    print(f"\nSenha gerada aleatoriamente: {senha}")
    confirmacao_senha = builtins.input("Confirme a senha: ")

    if senha != confirmacao_senha:
        print("Operação falhou! As senhas não conferem.")
        return

    cliente = Cliente(nome, cpf, data_nascimento, senha)
    usuarios.append(cliente)
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf: str, usuarios: list) -> Cliente:
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def autenticar_usuario(cpf: str, senha: str, usuarios: list) -> Cliente:
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Operação falhou! Usuário não encontrado.")
        return None

    if not usuario.verificar_senha(senha):
        print("Operação falhou! Senha incorreta.")
        return None

    return usuario


def listar_contas(contas: list):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['cliente']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def transferir_limite(conta_origem: Conta, valor: float):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return

    limite_disponivel = conta_origem.limite - conta_origem.saldo
    if valor > limite_disponivel:
        print(f"Operação falhou! Limite de transferência excedido (disponível: R$ {limite_disponivel:.2f}).")
        return

    conta_origem.saldo -= valor
    conta_origem.limite += valor
    atualiza_extrato(conta_origem, "Transferência de limite", valor)
    print(f"Transferência de limite realizada com sucesso! Saldo atual: R$ {conta_origem.saldo:.2f}")


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo usuário
    [nc]\tNova conta
    [lc]\tListar contas
    [t]\tTransferência
    [pg]\tPagamento de conta
    [login]\tLogin
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    contas = []
    usuarios = []
    conta_corrente = None
    extrato = ""

    while True:
        opcao = menu()

        if opcao == "d":
            if not conta_corrente:
                print("É necessário fazer login para realizar depósitos.")
                continue

            valor = float(builtins.input("Informe o valor do depósito: "))
            depositar(conta_corrente, valor)

        elif opcao == "s":
            if not conta_corrente:
                print("É necessário fazer login para realizar saques.")
                continue

            valor = float(builtins.input("Informe o valor do saque: "))
            sacar(conta_corrente, valor)

        elif opcao == "e":
            if not conta_corrente:
                print("É necessário fazer login para visualizar o extrato.")
                continue

            exibir_extrato(conta_corrente.saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            if not usuarios:
                print("É necessário criar um usuário antes de criar uma conta.")
                continue

            cliente = autenticar_usuario(cpf="00012345678", senha="123456", usuarios=usuarios)
            if not cliente:
                continue

            numero_conta = len(contas) + 1
            conta = criar_conta(cliente, numero_conta, contas)

            if conta:
                conta_corrente = conta
                print(f"Conta criada com sucesso! Número da conta: {conta.numero}")

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "t":
            if not conta_corrente:
                print("É necessário fazer login para realizar transferências.")
                continue

            valor = float(builtins.input("Informe o valor da transferência: "))
          
            print("\nSelecione o tipo de transferência:")
            print("[1] Transferência entre contas")
            print("[2] Transferência de limite")
            tipo_transferencia = builtins.input("Digite a opção desejada: ")

            if tipo_transferencia == "1":
                numero_conta_destino = int(builtins.input("Informe o número da conta destino: "))
                conta_destino = buscar_conta(numero_conta_destino, contas)

                if not conta_destino:
                    print("Operação falhou! Conta destino não encontrada.")
                    continue

                transferir(conta_corrente, conta_destino, valor)

            elif tipo_transferencia == "2":
                transferir_limite(conta_corrente, valor)

            else:
                print("Operação inválida! Selecione uma opção válida.")

        elif opcao == "pg":
            if not conta_corrente:
                print("É necessário fazer login para realizar pagamentos.")
                continue

            codigo_conta = builtins.input("Informe o código da conta a pagar: ")
            valor = float(builtins.input("Informe o valor do pagamento: "))
            pagar_conta(conta_corrente, codigo_conta, valor)

        elif opcao == "login":
            cpf = builtins.input("Informe o CPF: ")
            senha = builtins.input("Informe a senha: ")
            conta_corrente = autenticar_usuario(cpf, senha, usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

        extrato = ""


if __name__ == "__main__":
    main()
