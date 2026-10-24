import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.banco import BancoService

def main():
    banco = BancoService()

    while True:
        print("\n==============================")
        print("    SISTEMA BANCÁRIO IFPE    ")
        print("==============================")
        print("1. Cadastrar Conta")
        print("2. Consultar Saldo")
        print("3. Crédito")
        print("4. Débito")
        print("5. Transferência")
        print("0. Sair")
        print("==============================")
        
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                num = input("Número da conta: ")
                if banco.cadastrar_conta(num):
                    print("--> Conta cadastrada com sucesso!")
                else:
                    print("--> Erro: Conta já existe.")

            elif opcao == '2':
                num = input("Número da conta: ")
                saldo = banco.consultar_saldo(num)
                print(f"--> Saldo da conta {num}: R$ {saldo:.2f}")

            elif opcao == '3':
                num = input("Número da conta: ")
                valor = float(input("Valor do crédito: R$ "))
                banco.credito(num, valor)
                print("--> Crédito realizado com sucesso!")

            elif opcao == '4':
                num = input("Número da conta: ")
                valor = float(input("Valor do débito: R$ "))
                banco.debito(num, valor)
                print("--> Débito realizado com sucesso!")

            elif opcao == '5':
                origem = input("Número da conta de origem: ")
                destino = input("Número da conta de destino: ")
                valor = float(input("Valor da transferência: R$ "))
                banco.transferencia(origem, destino, valor)
                print("--> Transferência realizada com sucesso!")

            elif opcao == '0':
                print("Encerrando o sistema...")
                break
            else:
                print("--> Opção inválida!")
        except Exception as e:
            print(f"--> Erro na operação: {e}")

if __name__ == "__main__":
    main()