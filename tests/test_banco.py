import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.banco import BancoService, ContaBonus, ContaPoupanca, ContaSimples  # noqa: E402


class TestBancoService(unittest.TestCase):
    def setUp(self):
        self.banco = BancoService()

    # 1. Cadastrar Conta (por tipo de conta)
    def test_cadastrar_conta_simples(self):
        self.assertTrue(self.banco.cadastrar_conta_simples("001"))
        self.assertFalse(self.banco.cadastrar_conta_simples("001"))
        self.assertIsInstance(self.banco.contas["001"], ContaSimples)

    def test_cadastrar_conta_bonus(self):
        self.assertTrue(self.banco.cadastrar_conta_bonus("002"))
        self.assertFalse(self.banco.cadastrar_conta_bonus("002"))
        conta = self.banco.contas["002"]
        self.assertIsInstance(conta, ContaBonus)
        self.assertEqual(conta.pontos, 10)

    def test_cadastrar_conta_poupanca(self):
        self.assertTrue(self.banco.cadastrar_conta_poupanca("003", 250.0))
        self.assertFalse(self.banco.cadastrar_conta_poupanca("003", 100.0))
        conta = self.banco.contas["003"]
        self.assertIsInstance(conta, ContaPoupanca)
        self.assertEqual(conta.saldo, 250.0)

    # 2. Consultar Conta (por tipo de conta)
    def test_consultar_conta_simples(self):
        self.banco.cadastrar_conta_simples("101")
        dados = self.banco.consultar_dados_conta("101")
        self.assertEqual(dados["tipo"], "Conta Simples")
        self.assertEqual(dados["numero"], "101")
        self.assertEqual(dados["saldo"], 0.0)
        self.assertIsNone(dados["bonus"])

    def test_consultar_conta_bonus(self):
        self.banco.cadastrar_conta_bonus("102")
        dados = self.banco.consultar_dados_conta("102")
        self.assertEqual(dados["tipo"], "Conta Bônus")
        self.assertEqual(dados["numero"], "102")
        self.assertEqual(dados["saldo"], 0.0)
        self.assertEqual(dados["bonus"], 10)

    def test_consultar_conta_poupanca(self):
        self.banco.cadastrar_conta_poupanca("103", 500.0)
        dados = self.banco.consultar_dados_conta("103")
        self.assertEqual(dados["tipo"], "Conta Poupança")
        self.assertEqual(dados["numero"], "103")
        self.assertEqual(dados["saldo"], 500.0)
        self.assertIsNone(dados["bonus"])

    def test_consultar_conta_inexistente(self):
        with self.assertRaises(ValueError):
            self.banco.consultar_dados_conta("999")

    # 3. Consultar Saldo
    def test_consultar_saldo(self):
        self.banco.cadastrar_conta_poupanca("201", 320.5)
        self.assertEqual(self.banco.consultar_saldo("201"), 320.5)
        with self.assertRaises(ValueError):
            self.banco.consultar_saldo("999")

    # 4. Crédito
    def test_credito_caso_normal(self):
        self.banco.cadastrar_conta_simples("301")
        self.banco.credito("301", 150.0)
        self.assertEqual(self.banco.consultar_saldo("301"), 150.0)

    def test_credito_valor_negativo_nao_permitido(self):
        self.banco.cadastrar_conta_simples("301")
        with self.assertRaises(ValueError):
            self.banco.credito("301", -50.0)

    def test_credito_bonificacao_conta_bonus(self):
        self.banco.cadastrar_conta_bonus("302")
        self.banco.credito("302", 250.0)
        self.assertEqual(self.banco.consultar_saldo("302"), 250.0)
        self.assertEqual(self.banco.contas["302"].pontos, 12)

    # 5. Débito
    def test_debito_caso_normal(self):
        self.banco.cadastrar_conta_simples("401")
        self.banco.credito("401", 200.0)
        self.banco.debito("401", 80.0)
        self.assertEqual(self.banco.consultar_saldo("401"), 120.0)

    def test_debito_valor_negativo_nao_permitido(self):
        self.banco.cadastrar_conta_simples("401")
        with self.assertRaises(ValueError):
            self.banco.debito("401", -20.0)

    def test_debito_excede_limite_saldo_negativo(self):
        self.banco.cadastrar_conta_simples("401")
        with self.assertRaises(ValueError):
            self.banco.debito("401", 1000.01)

    # 6. Transferência
    def test_transferencia_valor_negativo_nao_permitido(self):
        self.banco.cadastrar_conta_simples("501")
        self.banco.cadastrar_conta_simples("502")
        with self.assertRaises(ValueError):
            self.banco.transferencia("501", "502", -100.0)

    def test_transferencia_excede_limite_saldo_origem(self):
        self.banco.cadastrar_conta_simples("501")
        self.banco.cadastrar_conta_simples("502")
        with self.assertRaises(ValueError):
            self.banco.transferencia("501", "502", 1000.01)

    def test_transferencia_bonificacao_conta_bonus_destino(self):
        self.banco.cadastrar_conta_poupanca("501", 1000.0)
        self.banco.cadastrar_conta_bonus("502")
        self.banco.transferencia("501", "502", 300.0)
        self.assertEqual(self.banco.consultar_saldo("501"), 700.0)
        self.assertEqual(self.banco.consultar_saldo("502"), 300.0)
        self.assertEqual(self.banco.contas["502"].pontos, 12)

    # 7. Render Juros
    def test_render_juros_conta_poupanca(self):
        self.banco.cadastrar_conta_poupanca("601", 200.0)
        self.banco.cadastrar_conta_poupanca("602", 100.0)
        self.banco.render_juros_poupanca("601", 10.0)
        self.banco.render_juros_poupanca("602", 5.0)
        self.assertAlmostEqual(self.banco.consultar_saldo("601"), 220.0)
        self.assertAlmostEqual(self.banco.consultar_saldo("602"), 105.0)


if __name__ == "__main__":
    unittest.main()
