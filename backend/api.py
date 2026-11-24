import os
import sys
from flask import Flask, jsonify, request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.banco import BancoService  # noqa: E402

app = Flask(__name__)
banco = BancoService()


@app.route("/banco/conta/", methods=["POST"])
def cadastrar_conta():
    data = request.get_json(force=True)
    tipo = (data.get("tipo") or "").strip().lower()
    numero = str(data.get("numero", "")).strip()

    if not numero:
        return jsonify({"erro": "Número da conta é obrigatório."}), 400

    if tipo == "simples":
        criada = banco.cadastrar_conta_simples(numero)
    elif tipo == "bonus":
        criada = banco.cadastrar_conta_bonus(numero)
    elif tipo == "poupanca":
        saldo_inicial = float(data.get("saldo_inicial", 0.0))
        criada = banco.cadastrar_conta_poupanca(numero, saldo_inicial)
    else:
        return jsonify({"erro": "Tipo de conta inválido (use: simples, bonus ou poupanca)."}), 400

    if not criada:
        return jsonify({"erro": "Conta já existe."}), 409

    return jsonify({"mensagem": "Conta cadastrada com sucesso.", "numero": numero, "tipo": tipo}), 201


@app.route("/banco/conta/", methods=["GET"])
def consultar_conta():
    numero = request.args.get("numero", "").strip()
    if not numero:
        return jsonify({"erro": "Informe o parâmetro 'numero'."}), 400
    try:
        dados = banco.consultar_dados_conta(numero)
        return jsonify(dados), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/banco/conta/<conta_id>/saldo", methods=["GET"])
def consultar_saldo(conta_id):
    try:
        saldo = banco.consultar_saldo(conta_id)
        return jsonify({"numero": conta_id, "saldo": saldo}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/banco/conta/<conta_id>/credito", methods=["PUT"])
def credito(conta_id):
    data = request.get_json(force=True)
    try:
        valor = float(data.get("valor"))
        banco.credito(conta_id, valor)
        return jsonify({"mensagem": "Crédito realizado com sucesso.", "saldo": banco.consultar_saldo(conta_id)}), 200
    except (TypeError, ValueError) as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/banco/conta/<conta_id>/debito", methods=["PUT"])
def debito(conta_id):
    data = request.get_json(force=True)
    try:
        valor = float(data.get("valor"))
        banco.debito(conta_id, valor)
        return jsonify({"mensagem": "Débito realizado com sucesso.", "saldo": banco.consultar_saldo(conta_id)}), 200
    except (TypeError, ValueError) as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/banco/conta/transferencia", methods=["PUT"])
def transferencia():
    data = request.get_json(force=True)
    try:
        origem = str(data.get("from", "")).strip()
        destino = str(data.get("to", "")).strip()
        valor = float(data.get("amount"))
        banco.transferencia(origem, destino, valor)
        return jsonify({"mensagem": "Transferência realizada com sucesso."}), 200
    except (TypeError, ValueError) as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/banco/conta/rendimento", methods=["PUT"])
def rendimento():
    data = request.get_json(force=True)
    try:
        numero = str(data.get("numero", "")).strip()
        taxa = float(data.get("taxa"))
        banco.render_juros_poupanca(numero, taxa)
        return jsonify({"mensagem": "Rendimento aplicado com sucesso.", "saldo": banco.consultar_saldo(numero)}), 200
    except (TypeError, ValueError, KeyError) as e:
        return jsonify({"erro": str(e)}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
