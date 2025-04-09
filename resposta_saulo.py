"""
Sistema Bancário Simples em Python
----------------------------------
Este programa simula um sistema bancário básico com as seguintes funcionalidades:
- Cadastro de usuários
- Abertura de contas bancárias
- Depósitos e saques
- Emissão de extratos
- Limite diário de saques

Desenvolvido para fins educacionais.
Autor: Saulo Pereira da Silva
Data: 08/04/2025
"""

clientes = []  # Lista de CPFs com conta
saldos = {}    # Dicionário: chave = CPF, valor = {'saldo': float, 'extrato': str, 'saques': int}
usuarios = []  # Lista de usuários
contas = []    # Lista de contas
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_SAQUE_VALOR = 100000

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("❌ Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("❌ Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("❌ Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("✅ Saque realizado com sucesso!")
    else:
        print("❌ Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def depositar(cpf, valor):
    if cpf not in clientes:
        print("❌ Usuário não possui conta. Depósito não permitido.")
        return
    if valor > 0:
        saldos[cpf]['saldo'] += valor
        saldos[cpf]['extrato'] += f"Depósito: R$ {valor:.2f}\n"
        print("✅ Depósito realizado com sucesso!")
    else:
        print("❌ Operação falhou! O valor informado é inválido.")

def exibir_extrato(cpf):
    if cpf not in clientes:
        print("❌ Usuário não possui conta.")
        return
    saldo = saldos[cpf]['saldo']
    extrato = saldos[cpf]['extrato']
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("==============================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("❌ Já existe usuário com esse CPF!")
        return
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, número, bairro, cidade/sigla-estado): ").strip()
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("✅ Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        if cpf in clientes:
            print("❌ Este CPF já possui conta.")
            return None
        clientes.append(cpf)
        saldos[cpf] = {"saldo": 0, "extrato": "", "saques": 0}
        print("✅ Conta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }
    else:
        print("❌ Usuário não encontrado, conta não criada.")
        return None

def listar_contas(contas):
    if not contas:
        print("❌ Nenhuma conta cadastrada.")
        return
    for conta in contas:
        linha = f"""\n==============================  
Agência: {conta['agencia']}
Número da Conta: {conta['numero_conta']}
Titular: {conta['usuario']['nome']}
=============================="""
        print(linha)

# MENU PRINCIPAL
menu = """
=========== MENU ===========
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair
============================

=> """

numero_conta = 1

while True:
    opcao = input(menu)

    if opcao == "d":
        cpf = input("Informe o CPF do titular da conta: ").strip()
        valor = float(input("Informe o valor do depósito: "))
        depositar(cpf, valor)

    elif opcao == "s":
        cpf = input("Informe o CPF do titular da conta: ").strip()
        if cpf not in clientes:
            print("❌ Usuário não possui conta.")
            continue
        valor = float(input("Informe o valor do saque: "))
        saldo_atual = saldos[cpf]["saldo"]
        extrato_atual = saldos[cpf]["extrato"]
        saques_realizados = saldos[cpf]["saques"]
        saldo_atual, extrato_atual, saques_realizados = sacar(
            saldo=saldo_atual,
            valor=valor,
            extrato=extrato_atual,
            limite=LIMITE_SAQUE_VALOR,
            numero_saques=saques_realizados,
            limite_saques=LIMITE_SAQUES,
        )
        saldos[cpf]["saldo"] = saldo_atual
        saldos[cpf]["extrato"] = extrato_atual
        saldos[cpf]["saques"] = saques_realizados

    elif opcao == "e":
        cpf = input("Informe o CPF do titular da conta: ").strip()
        exibir_extrato(cpf)

    elif opcao == "nu":
        criar_usuario(usuarios)

    elif opcao == "nc":
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)
            numero_conta += 1

    elif opcao == "lc":
        listar_contas(contas)

    elif opcao == "q":
        print("👋 Saindo... Obrigado por utilizar nosso sistema!")
        break

    else:
        print("❌ Operação inválida. Por favor, selecione uma opção válida.")
