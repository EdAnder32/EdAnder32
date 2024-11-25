from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Função para verificar e adicionar o nome no arquivo
def register_master_look_up(nome):
    file_path = 'users_master_look.txt'

    # Verifica se o arquivo existe, se não, cria o arquivo com a linha inicial para contar os usuários
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("0\n")  # Primeira linha com o número de usuários

    # Lê o arquivo e verifica se o nome já está presente
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # A primeira linha contém o número de usuários
    user_count = int(lines[0].strip())

    # Verifica se o nome já existe no arquivo
    if nome + '\n' in lines:
        return jsonify({"message": "Nome já registrado!"}), 400

    # Se o nome não existir, adiciona na lista e atualiza o contador de usuários
    with open(file_path, 'a') as file:
        file.write(f"{nome}\n")

    # Atualiza o número total de usuários
    user_count += 1
    with open(file_path, 'r+') as file:
        lines[0] = f"{user_count}\n"  # Atualiza a primeira linha com o novo número de usuários
        file.seek(0)  # Move o ponteiro de leitura para o início do arquivo
        file.writelines(lines)

    return jsonify({"message": f"Usuário '{nome}' registrado com sucesso!"}), 200

@app.route('/register_master_look_up', methods=['POST'])
def register():
    # Obtém o parâmetro 'username' do formulário (usando request.form)
    nome = request.form.get('username')

    if not nome:
        return jsonify({"message": "Nome não fornecido!"}), 400

    if len(nome) > 12:
        return jsonify({"message": "Nome não pode ser maior que 12 caracteres!"}), 400

    # Chama a função para registrar o nome
    return register_master_look_up(nome)

if __name__ == '__main__':
    app.run(debug=True)

