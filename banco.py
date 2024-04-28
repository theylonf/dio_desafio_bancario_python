def verifica_saldo(valor):
  return saldo >= valor

def verifica_limite_saques():
  return numero_saques >= LIMITE_SAQUES

def atualiza_extrato(acao, valor):
  global extrato
  extrato += f"{acao}: R$ {valor:.2f}\n"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
  opcao = input(f"""
  [d] Depositar (Saldo atual: R$ {saldo:.2f})
  [s] Sacar
  [e] Extrato
  [q] Sair

  => """).lower()

  if opcao == "d":
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
      atualiza_extrato("Depósito", valor)
      saldo += valor
    else:
      print("Operação falhou! O valor informado é inválido.")

  elif opcao == "s":
    valor = float(input("Informe o valor do saque: "))

    if not verifica_saldo(valor):
      print("Operação falhou! Saldo insuficiente.")
    elif verifica_limite_saques():
      print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
      atualiza_extrato("Saque", valor)
      saldo -= valor
      numero_saques += 1
    else:
      print("Operação falhou! O valor informado é inválido.")

  elif opcao == "e":
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

  elif opcao == "q":
    break

  else:
    print("Operação inválida, por favor selecione novamente a operação desejada.")
