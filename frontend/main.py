import requests

BASE_URL = "http://127.0.0.1:5000"


def exibir_menu() -> None:
    print("\n---- SISTEMA BANCÁRIO (PROJETO 2 - REST) ----")
    print("1. Cadastrar Conta Simples")
    print("2. Cadastrar Conta Bônus")
    print("3. Cadastrar Conta Poupança")
    print("4. Consultar Saldo")
    print("5. Crédito (Depósito)")
    print("6. Débito (Saque)")
    print("7. Transferência")
    print("8. Render Juros (Conta Poupança)")
    print("9. Consultar Dados Completos da Conta")
    print("0. Sair")


def cadastrar_conta(tipo: str) -> None:
    numero = input("Número da conta: ").strip()
    payload = {"tipo": tipo, "numero": numero}

    if tipo == "poupanca":
        saldo_inicial = float(input("Saldo inicial da Conta Poupança: "))
        payload["saldo_inicial"] = saldo_inicial

    resp = requests.post(f"{BASE_URL}/banco/conta/", json=payload, timeout=5)
    dados = resp.json()
    if resp.status_code in (200, 201):
        print(dados.get("mensagem", "Conta cadastrada com sucesso."))
    else:
        print(f"Erro: {dados.get('erro', 'Falha ao cadastrar conta.')}")


def consultar_saldo() -> None:
    conta_id = input("Número da conta: ").strip()
    resp = requests.get(f"{BASE_URL}/banco/conta/{conta_id}/saldo", timeout=5)
    dados = resp.json()
    if resp.status_code == 200:
        print(f"Saldo atual da conta {dados['numero']}: R$ {dados['saldo']:.2f}")
    else:
        print(f"Erro: {dados.get('erro', 'Conta não encontrada.')}")


def operacao_valor(conta_id: str, acao: str, valor: float) -> None:
    resp = requests.put(
        f"{BASE_URL}/banco/conta/{conta_id}/{acao}",
        json={"valor": valor},
        timeout=5,
    )
    dados = resp.json()
    if resp.status_code == 200:
        print(dados.get("mensagem", "Operação concluída."))
        if "saldo" in dados:
            print(f"Novo saldo: R$ {dados['saldo']:.2f}")
    else:
        print(f"Erro: {dados.get('erro', 'Falha na operação.')}")


def transferencia() -> None:
    origem = input("Conta de origem: ").strip()
    destino = input("Conta de destino: ").strip()
    valor = float(input("Valor da transferência: "))

    payload = {
        "from": origem,
        "to": destino,
        "amount": valor,
    }
    resp = requests.put(f"{BASE_URL}/banco/conta/transferencia", json=payload, timeout=5)
    dados = resp.json()
    if resp.status_code == 200:
        print(dados.get("mensagem", "Transferência realizada com sucesso."))
    else:
        print(f"Erro: {dados.get('erro', 'Falha na transferência.')}")


def render_juros() -> None:
    numero = input("Número da Conta Poupança: ").strip()
    taxa = float(input("Taxa de juros (%): "))

    resp = requests.put(
        f"{BASE_URL}/banco/conta/rendimento",
        json={"numero": numero, "taxa": taxa},
        timeout=5,
    )
    dados = resp.json()
    if resp.status_code == 200:
        print(dados.get("mensagem", "Rendimento aplicado com sucesso."))
        if "saldo" in dados:
            print(f"Novo saldo: R$ {dados['saldo']:.2f}")
    else:
        print(f"Erro: {dados.get('erro', 'Falha ao aplicar rendimento.')}")


def consultar_dados_conta() -> None:
    numero = input("Número da conta a consultar: ").strip()
    resp = requests.get(f"{BASE_URL}/banco/conta/", params={"numero": numero}, timeout=5)
    dados = resp.json()

    if resp.status_code == 200:
        print("\n--- DADOS DA CONTA ---")
        print(f"Tipo: {dados['tipo']}")
        print(f"Número: {dados['numero']}")
        print(f"Saldo: R$ {dados['saldo']:.2f}")
        if dados.get("bonus") is not None:
            print(f"Bônus (Pontos): {dados['bonus']}")
    else:
        print(f"Erro: {dados.get('erro', 'Conta não encontrada.')}")


def main() -> None:
    while True:
        print("\n--- SISTEMA BANCÁRIO (VERSÃO 2.0) ---")
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
            if opcao == "1":
                cadastrar_conta("simples")
            elif opcao == "2":
                cadastrar_conta("bonus")
            elif opcao == "3":
                cadastrar_conta("poupanca")
            elif opcao == "4":
                consultar_saldo()
            elif opcao == "5":
                conta_id = input("Número da conta: ").strip()
                valor = float(input("Valor do crédito: "))
                operacao_valor(conta_id, "credito", valor)
            elif opcao == "6":
                conta_id = input("Número da conta: ").strip()
                valor = float(input("Valor do débito: "))
                operacao_valor(conta_id, "debito", valor)
            elif opcao == "7":
                transferencia()
            elif opcao == "8":
                render_juros()
            elif opcao == "9":
                consultar_dados_conta()
            elif opcao == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida.")
        except ValueError:
            print("Erro: informe um valor numérico válido.")
        except requests.exceptions.ConnectionError:
            print(
                "Erro: não foi possível conectar à API em http://127.0.0.1:5000. "
                "Verifique se backend/api.py está rodando."
            )
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")


if __name__ == "__main__":
    main()
