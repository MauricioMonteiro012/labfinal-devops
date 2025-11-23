"""
Aplicação Flask para o desafio DevOps
API simples com endpoints para demonstração
"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Configuração
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Simulação de banco de dados em memória
users_db = []
tasks_db = []


class User:
    """Classe para representar um usuário"""
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Task:
    """Classe para representar uma tarefa"""
    def __init__(self, id, title, description, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }


@app.route('/')
def home():
    """Endpoint raiz da API"""
    return jsonify({
        'message': 'Bem-vindo à API DevOps Challenge',
        'version': '1.0.0',
        'status': 'running'
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'devops-challenge-api'
    }), 200


@app.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários"""
    return jsonify([user.to_dict() for user in users_db]), 200


@app.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Nome e email são obrigatórios'}), 400
    
    # Validação de email simples
    if '@' not in data.get('email', ''):
        return jsonify({'error': 'Email inválido'}), 400
    
    user_id = len(users_db) + 1
    user = User(user_id, data['name'], data['email'])
    users_db.append(user)
    
    return jsonify(user.to_dict()), 201


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna um usuário específico"""
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retorna todas as tarefas"""
    return jsonify([task.to_dict() for task in tasks_db]), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    """Cria uma nova tarefa"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Título é obrigatório'}), 400
    
    task_id = len(tasks_db) + 1
    task = Task(
        task_id,
        data['title'],
        data.get('description', ''),
        data.get('completed', False)
    )
    tasks_db.append(task)
    
    return jsonify(task.to_dict()), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retorna uma tarefa específica"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualiza uma tarefa"""
    task = next((t for t in tasks_db if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    data = request.get_json()
    
    if data.get('title'):
        task.title = data['title']
    if data.get('description') is not None:
        task.description = data['description']
    if data.get('completed') is not None:
        task.completed = data['completed']
    
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deleta uma tarefa"""
    global tasks_db
    task = next((t for t in tasks_db if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    tasks_db = [t for t in tasks_db if t.id != task_id]
    return jsonify({'message': 'Tarefa deletada com sucesso'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

