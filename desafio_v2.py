# Importação de módulos necessários para obter o horário dos saques
from datetime import datetime
import pytz

# Função de menu()
#
# Funções de Saque(), Depósito() e Extrato()

# Declaração de algumas variáveis e constantes necessárias
LIMITE = 500
quantidade_saques = 0
saldo = 0
lista_saques = []
LIMITE_SAQUES = 3 # 3

lista_usuarios = []
lista_contas = []
conta = 0

# Opções do menu
def menu():

    while True:
        menu = """

        Selecione uma opção.

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo usuário (Cliente)
        [nc] Nova conta
        [lu] Listar usuários
        [q] Sair

        =>"""

        opcao = input(menu).lower() # Obter a opção do usuário

        # Opção de depósito
        if opcao == 'd':
            valor = input('Insira um valor a depositar: R$')
            mensagem = deposito(valor)
            print(mensagem)

        elif opcao == 's': # Opção de saque
            valor_saque = input('Insira um valor para ser sacado: R$')
            mensagem = saque(valor_saque=valor_saque)
            print(mensagem)

        elif opcao == 'e': # Opção de extrato
            extrato(saldo, extrato=lista_saques)

        elif opcao == 'nu': # Opção para cadastrar novo usuário (cliente)
            mensagem = criar_usuario()
            print(mensagem)

        elif opcao == 'nc': # Opção para criar uma nova conta de cliente
            cpf_usuario = str(input('Insira o CPF do cliente: '))
            mensagem = criar_conta(cpf_usuario)
            print(mensagem)

        elif opcao == 'lu': # Opção para listar os clientes
            listar_contas()

        elif opcao == 'q': # Opção de sair do sistema
            print('Saindo da conta! Obrigado por nos acessar!')
            break

        else:
            print('Operação inválida etc...')


def saque(*, valor_saque: str):
    global saldo, LIMITE_SAQUES, quantidade_saques

    valor_base_saque = valor_saque.replace(',', '.')

    # Checa se o valor contém números para converter para float
    if valor_base_saque.replace('.', '', 1).isdigit():
        valor_a_sacar = float(valor_base_saque)

        # Sequência de if/elif/else para realizar as operações necessárias
        # e tratar os erros
        if saldo > 0 and valor_a_sacar > 0:
            if valor_a_sacar <= saldo and LIMITE_SAQUES > 0 and valor_a_sacar <= LIMITE:
                saldo -= valor_a_sacar
                LIMITE_SAQUES -= 1
                quantidade_saques += 1

                lista_saques.append({
                    'Valor Sacado': valor_a_sacar,
                    'Data do Saque': datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d/%m/%Y, %H:%M')
                })

                return f'Saque realizado! Novo saldo R${saldo:.2f}'  # Retorna a mensagem de sucesso

            elif LIMITE_SAQUES == 0:
                return 'Você atingiu seu LIMITE diário de saques! Tente amanhã'

            elif valor_a_sacar > LIMITE:
                return f'Não é possível sacar um valor maior que seu LIMITE atual de R${LIMITE:.2f}'

            else:
                return 'Saldo insuficiente!'

        else:
            return 'Erro! Saldo insuficiente ou valor a sacar inválido!'

    else:
        return 'Erro! Valor a sacar inválido!'


def deposito(valor_base: str, /):
    while True:
        valor_base = valor_base.replace(',', '.')

        # Checa se o valor contém números para converter para float
        if valor_base.replace('.', '', 1).isdigit():
            valor_a_depositar = float(valor_base)

            if valor_a_depositar > 0:
                global saldo
                saldo += valor_a_depositar
                return f'O valor de RS{valor_a_depositar:.2f} foi depositado! Saldo {saldo}'

            print('Erro! Insira um valor positivo.')

        else:
            print('Erro! Insira apenas números!')
            break


def extrato(saldo: float, /, extrato=None):
    if extrato is None:
        extrato = []  # lista vazia se o extrato não for passado

    if not extrato:
        print('Não houveram movimentações')

    else:
        print('=== Extrato da conta bancária ===')
        print(f'Saldo disponível: R${saldo:.2f}')
        print(f'Quantidade de saques realizados: {len(extrato)}')
        print()

        for saque in extrato:
            print('-' * 30)
            for chave, valor in saque.items():
                if chave == 'Valor Sacado':
                    print(f'{chave}: R${valor:.2f}')
                else:
                    print(f'{chave}: {valor}')
            print('-' * 30)


def criar_usuario():
    cpf_existente = False

    print('=== Cadastro de usuário ===')

    while True:
        nome_usuario = str(input('Insira um nome de usuário: ')).capitalize()

        while not nome_usuario.isalpha():
            nome_usuario = str(input('Erro! Insira um nome válido!: '))

        data_de_nascimento = str(input('Insira uma data de nascimento (dd/mm/aaaa): '))

        while True:
            cpf = input('Insira um CPF: ').replace('.', '').replace('-', '')

            if cpf.isnumeric():
                break
            else:
                print('Erro! O CPF deve conter apenas números.')

        for cliente in lista_usuarios:
            if cliente['CPF'] == cpf:
                cpf_existente = True
                return 'CPF já cadastrado!'
                #break

        if not cpf_existente:  # Se o CPF não for encontrado, cadastra o cliente
            endereço = str(input('Insira um endereço no formato logradouro, nro, bairro, cidade/sigla do estado: '))

            lista_usuarios.append({
                'Nome do Cliente': nome_usuario,
                'Data de Nascimento': data_de_nascimento,
                'CPF': cpf,
                'Endereço': endereço
            })

            return 'Cliente cadastrado com sucesso!'


def criar_conta(cpf_usuario: str):
    # Aqui, o usuário é vinculado ao seu CPF
    global conta

    while True:
        cpf = cpf_usuario

        for cliente in lista_usuarios:
            if cliente['CPF'] == cpf:
                agencia = '0001'
                conta += 1

                lista_contas.append({
                    'Agencia': agencia,
                    'Conta': conta,
                    'CPF': cpf
                })

                return 'Conta criada com sucesso!'

        return 'Erro! Cliente não existe!'


def listar_contas():
    if not lista_usuarios:
        print('Não há clientes cadastrados')

    else:
        print('=== Lista de Clientes ===')
        print()

        for cliente in lista_usuarios:
            print('-' * 30)
            for chave, valor in cliente.items():
                print(f'{chave}: {valor}')

            print('-' * 30)

# ===== Código Cliente =====
menu()
