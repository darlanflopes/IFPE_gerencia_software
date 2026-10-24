class Conta:
    def __init__(self, numero: int):
        self.numero = numero
        self.saldo = 0  # Saldo inicial zerado
class BancoService:
    def __init__(self):
        self.contas = {}  # Persistência em memória
    def cadastrar_conta(self, numero: int) -> bool:
        if numero in self.contas:
            return False
        self.contas[numero] = Conta(numero)
        return True
    def consultar_saldo(self, numero: int) -> int:
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        return self.contas[numero].saldo
    def credito(self, numero: int, valor: int):
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        if valor <= 0:
            raise ValueError("O valor do crédito deve ser positivo.")
        self.contas[numero].saldo += valor
    def debito(self, numero: int, valor: int):
        if numero not in self.contas:
            raise ValueError("Conta não encontrada.")
        if valor <= 0:
            raise ValueError("O valor do débito deve ser positivo.")
        # Permite saldo negativo
        self.contas[numero].saldo -= valor
    def transferencia(self, origem: int, destino: int, valor: int):
        if origem not in self.contas or destino not in self.contas:
            raise ValueError("Conta de origem ou destino não encontrada.")
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        
        self.debito(origem, valor)
        self.credito(destino, valor)