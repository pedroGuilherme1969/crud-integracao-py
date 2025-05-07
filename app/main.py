from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = []

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    obrigatorios = ['nome', 'email', 'senha', 'cpf']
    if not all(campo in dados for campo in obrigatorios):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400
    if any(u['cpf'] == dados['cpf'] for u in usuarios):
        return jsonify({'erro': 'CPF já cadastrado'}), 400
    usuarios.append(dados)
    return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios), 200

@app.route('/usuarios/<cpf>', methods=['GET'])
def buscar_usuario(cpf):
    for u in usuarios:
        if u['cpf'] == cpf:
            return jsonify(u), 200
    return jsonify({'erro': 'Usuário não encontrado'}), 404

@app.route('/usuarios/<cpf>', methods=['DELETE'])
def deletar_usuario(cpf):
    for u in usuarios:
        if u['cpf'] == cpf:
            usuarios.remove(u)
            return jsonify({'mensagem': 'Usuário removido com sucesso'}), 200
    return jsonify({'erro': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
