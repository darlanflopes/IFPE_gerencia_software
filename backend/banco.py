class Conta:
    def __init__(self, numero: int):
        self.numero = numero
        self.saldo = 0  # Saldo inicial zerado
class BancoService:
    def __init__(self):
        self.contas = {}  # Persistência em memória