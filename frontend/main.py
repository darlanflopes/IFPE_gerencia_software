import sys
import os

# Adiciona o diretório raiz ao path para importar o backend corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.banco import BancoService, ContaBonus

def main():
    banco = BancoService()

    while True:
        print("\n--- SISTEMA BANCÁRIO (VERSÃO 2) ---")
        print("1. Cadastrar Conta Simples")
        print("2. Cadastrar Conta Bônus")
        print("3. Cadastrar Conta Poupança")
        print("4. Consultar Saldo")
        print("5. Crédito (Depósito)")
        print("6. Débito (Saque)")
        print("7. Transferência")
        print("8. Render Juros (Conta Poupança)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                num = input("Número da conta simples: ")
                if banco.cadastrar_conta_simples(num):
                    print("Conta simples cadastrada com sucesso!")
                else:
                    print("Erro: Conta já existe.")

            elif opcao == '2':
                num = input("Número da conta bônus: ")
                if banco.cadastrar_conta_bonus(num):
                    print("Conta bônus cadastrada com sucesso! (Inicia com 10 pontos)")
                else:
                    print("Erro: Conta já existe.")

            elif opcao == '3':
                num = input("Número da conta poupança: ")
                if banco.cadastrar_conta_poupanca(num):
                    print("Conta poupança cadastrada com sucesso!")
                else:
                    print("Erro: Conta já existe.")

            elif opcao == '4':
                num = input("Número da conta: ")
                saldo = banco.consultar_saldo(num)
                conta = banco.contas[num]
                # Se for conta bônus, exibe também os pontos acumulados
                if isinstance(conta, ContaBonus):
                    print(f"Saldo atual: R$ {saldo:.2f} | Pontos Bônus: {conta.pontos}")
                else:
                    print(f"Saldo atual: R$ {saldo:.2f}")

            elif opcao == '5':
                num = input("Número da conta: ")
                valor = float(input("Valor do crédito: "))
                banco.credito(num, valor)
                print("Crédito realizado com sucesso!")
                conta = banco.contas[num]
                if isinstance(conta, ContaBonus):
                    print(f"Pontuação atualizada da Conta Bônus: {conta.pontos} pontos.")

            elif opcao == '6':
                num = input("Número da conta: ")
                valor = float(input("Valor do débito: "))
                banco.debito(num, valor)
                print("Débito realizado com sucesso!")

            elif opcao == '7':
                origem = input("Número da conta de origem: ")
                destino = input("Número da conta de destino: ")
                valor = float(input("Valor da transferência: "))
                banco.transferencia(origem, destino, valor)
                print("Transferência realizada com sucesso!")
                conta_dest = banco.contas[destino]
                if isinstance(conta_dest, ContaBonus):
                    print(f"Conta de destino é Bônus. Pontuação atualizada: {conta_dest.pontos} pontos.")

            elif opcao == '8':
                num = input("Número da conta poupança: ")
                taxa = float(input("Informe a taxa de juros em percentagem (ex: 10.5 para 10.5%): "))
                banco.render_juros_poupanca(num, taxa)
                print("Juros aplicados com sucesso à Conta Poupança!")
                saldo_atualizado = banco.consultar_saldo(num)
                print(f"Novo saldo após juros: R$ {saldo_atualizado:.2f}")

            elif opcao == '0':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()
