from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from models.aluno import db, Aluno

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Rota para adicionar aluno
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    print("dados recebidos:", data)
    novo_aluno = Aluno(
        nome=data['nome'],
        email=data['email'],
        matricula=data['matricula'],
        senha=data['senha']
    )
    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({"message": "Aluno cadastrado com sucesso!"}), 201


# Rota para listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    # Obtém todos os alunos do banco de dados
    alunos = Aluno.query.all()

    # Converte os alunos em um formato de dicionário
    alunos_lista = [
        {
            "id": aluno.id,
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": aluno.matricula
        }
        for aluno in alunos
    ]

    # Retorna a lista de alunos e o total
    return jsonify({
        "alunos": alunos_lista,
        "total_alunos": len(alunos_lista)  # Conta o total de alunos
    })


# Buscar um aluno por ID
@app.route('/alunos/<int:id>', methods=['GET'])
def buscar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado"}), 404
    return jsonify(aluno.to_dict())

# Atualizar aluno
@app.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado"}), 404

    data = request.get_json()
    aluno.nome = data['nome']
    aluno.email = data['email']
    aluno.matricula = data['matricula']
    aluno.senha = data['senha']
    db.session.commit()
    return jsonify({"message": "Aluno atualizado com sucesso!"})

# Deletar aluno
@app.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno deletado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
