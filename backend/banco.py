class Conta:
    def __init__(self, numero: str):
        self.numero = numero
        self.saldo = 0.0

class ContaSimples(Conta):
    def __init__(self, numero: str):
        super().__init__(numero)


class ContaBonus(Conta):
    def __init__(self, numero: str):
        super().__init__(numero)
        self.pontos = 10  # Pontuação inicial de 10 pontos


class ContaPoupanca(Conta):
    def __init__(self, numero: str):
        super().__init__(numero)

    def render_juros(self, taxa: float):
        if taxa < 0:
            raise ValueError("A taxa de juros não pode ser negativa.")
        # Acrescenta os juros ao saldo com base na taxa percentual informada (ex: 10.5%)
        self.saldo += self.saldo * (taxa / 100.0)


class BancoService:
    def __init__(self):
        self.contas = {}  # Armazena as contas em memória

    def cadastrar_conta_simples(self, numero: str, saldo_inicial: float = 0.0) -> bool:
        if numero in self.contas:
            return False
        conta = Conta(numero)
        conta.saldo = saldo_inicial  # Informa o saldo inicial na criação
        self.contas[numero] = conta
        return True

    def cadastrar_conta_bonus(self, numero: str) -> bool:
        if numero in self.contas:
            return False
        self.contas[numero] = ContaBonus(numero)
        return True

    def cadastrar_conta_poupanca(self, numero: str, saldo_inicial: float = 0.0) -> bool:
        if numero in self.contas:
            return False
        self.contas[numero] = ContaPoupanca(numero, saldo_inicial)
        return True

    def consultar_saldo(self, numero: str) -> float:
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        return self.contas[numero].saldo

    def credito(self, numero: str, valor: float):
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        if valor <= 0:
            raise ValueError("O valor do crédito deve ser positivo.")
        
        self.contas[numero].saldo += valor
        
        # Regra da Conta Bônus para Depósitos: 1 ponto para cada R$ 100,00
        if isinstance(self.contas[numero], ContaBonus):
            pontos_ganhos = int(valor // 100)
            self.contas[numero].pontos += pontos_ganhos

    def debito(self, numero: str, valor: float):
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        if valor <= 0:
            raise ValueError("O valor do débito deve ser positivo.")
        
        conta = self.contas[numero]
        
        # Requisito 2 da Versão 3: Conta Simples e Conta Bônus permitem saldo negativo até -1000.00
        if isinstance(conta, (ContaSimples, ContaBonus)) or type(conta) is Conta:
            if conta.saldo - valor < -1000.00:
                raise ValueError("Limite máximo de saldo negativo excedido (R$ -1.000,00).")
        else:
            # Conta Poupança não permite saldo negativo (ou segue a regra padrão restrita)
            if conta.saldo - valor < 0:
                raise ValueError("Saldo insuficiente para realizar o débito.")
                
        conta.saldo -= valor

    def transferencia(self, origem: str, destino: str, valor: float):
        if origem not in self.contas or destino not in self.contas:
            raise ValueError("Conta de origem ou destino não encontrada.")
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        
        conta_origem = self.contas[origem]
        
        # Validação de limite de saldo negativo na origem para Simples e Bônus (-1000.00)
        if isinstance(conta_origem, (ContaSimples, ContaBonus)):
            if conta_origem.saldo - valor < -1000.00:
                raise ValueError("Limite máximo de saldo negativo excedido na conta de origem (R$ -1.000,00).")
        else:
            if conta_origem.saldo - valor < 0:
                raise ValueError("Saldo insuficiente na conta de origem.")

        # Realiza o débito na origem e o crédito no destino
        self.debito(origem, valor)
        self.credito(destino, valor)

        # Regra atualizada da Conta Bônus para Transferências Recebidas: 1 ponto a cada R$ 150,00 reais
        if isinstance(self.contas[destino], ContaBonus):
            pontos_ganhos = int(valor // 150)
            self.contas[destino].pontos += pontos_ganhos

    def render_juros_poupanca(self, numero: str, taxa: float):
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        if not isinstance(self.contas[numero], ContaPoupanca):
            raise TypeError("Esta operação é permitida APENAS para Contas Poupança.")
        self.contas[numero].render_juros(taxa)