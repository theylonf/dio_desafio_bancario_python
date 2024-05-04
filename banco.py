def verifica_saldo(valor, saldo):
    return saldo >= valor

def verifica_limite_saques(numero_saques, limite_saques):
    return numero_saques >= limite_saques

def atualiza_extrato(acao, valor, extrato):
    extrato += f"{acao}: R$ {valor:.2f}\n"
    return extrato

def cadastrar_usuario():
    nome = input("Informe o nome do usuário: ")
    cpf = input("Informe o CPF do usuário: ")
    # Aqui você pode adicionar mais informações para cadastrar o usuário
    return nome, cpf

def cadastrar_conta_bancaria():
    numero_conta = input("Informe o número da conta bancária: ")
    tipo_conta = input("Informe o tipo da conta (corrente/poupança): ")
    # Aqui você pode adicionar mais informações para cadastrar a conta bancária
    return numero_conta, tipo_conta

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3

while True:
    opcao = input(f"""
    [d] Depositar (Saldo atual: R$ {saldo:.2f})
    [s] Sacar
    [e] Extrato
    [c] Cadastrar usuário
    [a] Cadastrar conta bancária
    [q] Sair

    => """).lower()

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            extrato = atualiza_extrato("Depósito", valor, extrato)
            saldo += valor
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        if not verifica_saldo(valor, saldo):
            print("Operação falhou! Saldo insuficiente.")
        elif verifica_limite_saques(numero_saques, limite_saques):
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            extrato = atualiza_extrato("Saque", valor, extrato)
            saldo -= valor
            numero_saques += 1
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "c":
        nome, cpf = cadastrar_usuario()
        print(f"Usuário {nome} cadastrado com sucesso!")

    elif opcao == "a":
        numero_conta, tipo_conta = cadastrar_conta_bancaria()
        print(f"Conta bancária {numero_conta} do tipo {tipo_conta} cadastrada com sucesso!")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
