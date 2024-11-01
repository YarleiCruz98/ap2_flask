from flask import Blueprint, jsonify, request
from models.ap2_escola_models import db, Professor, Aluno, Turma
from datetime import datetime

school_blueprint = Blueprint('school', __name__)

# Rotas para Professores
@school_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores])

@school_blueprint.route('/professores/<int:id>', methods=['GET'])
def get_professor(id):
    professor = Professor.query.get(id)
    if professor:
        return jsonify(professor.to_dict())
    return jsonify({'message': 'Professor não encontrado'}), 404

@school_blueprint.route('/professores', methods=['POST'])
def create_professor():
    data = request.form
    new_professor = Professor(
        nome=data['nome'],
        idade=data['idade'],
        materia=data['materia'],
        observacoes=data.get('observacoes')
    )
    db.session.add(new_professor)
    db.session.commit()
    return jsonify(new_professor.to_dict()), 201

@school_blueprint.route('/professores/<int:id>', methods=['PUT'])
def update_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404

    data = request.form
    professor.nome = data.get('nome', professor.nome)
    professor.idade = data.get('idade', professor.idade)
    professor.materia = data.get('materia', professor.materia)
    professor.observacoes = data.get('observacoes', professor.observacoes)
    db.session.commit()
    return jsonify(professor.to_dict())

@school_blueprint.route('/professores/<int:id>', methods=['DELETE'])
def delete_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({'message': 'Professor não encontrado'}), 404

    db.session.delete(professor)
    db.session.commit()
    return jsonify({'message': 'Professor deletado com sucesso'})

# Rotas para Turmas
@school_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas])

@school_blueprint.route('/turmas/<int:id>', methods=['GET'])
def get_turma(id):
    turma = Turma.query.get(id)
    if turma:
        return jsonify(turma.to_dict())
    return jsonify({'message': 'Turma não encontrada'}), 404

@school_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    data = request.form
    ativo = data.get('ativo', 'true').lower() == 'true'  # Converte para booleano
    new_turma = Turma(
        descricao=data['descricao'],
        ativo=ativo,
        professor_id=data['professor_id']
    )
    db.session.add(new_turma)
    db.session.commit()
    return jsonify(new_turma.to_dict()), 201

@school_blueprint.route('/turmas/<int:id>', methods=['PUT'])
def update_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'message': 'Turma não encontrada'}), 404

    data = request.form
    turma.descricao = data.get('descricao', turma.descricao)
    turma.ativo = data.get('ativo', turma.ativo)
    turma.professor_id = data.get('professor_id', turma.professor_id)
    db.session.commit()
    return jsonify(turma.to_dict())

@school_blueprint.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'message': 'Turma não encontrada'}), 404

    db.session.delete(turma)
    db.session.commit()
    return jsonify({'message': 'Turma deletada com sucesso'})

# Rotas para Alunos
@school_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return jsonify([a.to_dict() for a in alunos])

@school_blueprint.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = Aluno.query.get(id)
    if aluno:
        return jsonify(aluno.to_dict())
    return jsonify({'message': 'Aluno não encontrado'}), 404

@school_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.form
    try:
        # Converte a string de data_nascimento para um objeto date
        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        new_aluno = Aluno(
            nome=data['nome'],
            idade=data['idade'],
            data_nascimento=data_nascimento,
            turma_id=data['turma_id']
        )
        
        db.session.add(new_aluno)
        db.session.commit()
        return jsonify(new_aluno.to_dict()), 201
    except ValueError as e:
        return jsonify({'message': 'Data de nascimento inválida'}), 400
    except Exception as e:
        return jsonify({'message': 'Erro ao criar aluno: {}'.format(str(e))}), 500

@school_blueprint.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    data = request.form
    aluno.nome = data.get('nome', aluno.nome)
    aluno.idade = data.get('idade', aluno.idade)
    aluno.turma_id = data.get('turma_id', aluno.turma_id)
    db.session.commit()
    return jsonify(aluno.to_dict())

@school_blueprint.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno deletado com sucesso'})