"""
Aplicação Flask para o desafio DevOps
API simples com endpoints para demonstração
"""
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS
import os

app = Flask(__name__)

# Habilitar CORS para todas as rotas
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger"
}

# Obter host dinamicamente
host = os.environ.get("SWAGGER_HOST", "localhost:5000")
if "://" in host:
    host = host.split("://")[-1]

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "DevOps Challenge API",
        "description": "API REST para gerenciamento de usuários e tarefas",
        "version": "1.0.0"
    },
    "host": host,
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Configuração
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
    """
    Endpoint raiz da API
    ---
    tags:
      - Geral
    responses:
      200:
        description: Informações da API
        schema:
          type: object
          properties:
            message:
              type: string
            version:
              type: string
            status:
              type: string
    """
    return jsonify({
        'message': 'Bem-vindo à API DevOps Challenge',
        'version': '1.0.0',
        'status': 'running'
    })


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check
    ---
    tags:
      - Geral
    responses:
      200:
        description: Status de saúde da API
        schema:
          type: object
          properties:
            status:
              type: string
            service:
              type: string
    """
    return jsonify({
        'status': 'healthy',
        'service': 'devops-challenge-api'
    }), 200


@app.route('/users', methods=['GET'])
def get_users():
    """
    Retorna todos os usuários
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de todos os usuários
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
    """
    return jsonify([user.to_dict() for user in users_db]), 200


@app.route('/users', methods=['POST'])
def create_user():
    """
    Cria um novo usuário
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: UserCreate
          required:
            - name
            - email
          properties:
            name:
              type: string
              example: João Silva
              description: Nome completo do usuário
            email:
              type: string
              example: joao@example.com
              description: Email do usuário
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          id: UserResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: João Silva
            email:
              type: string
              example: joao@example.com
      400:
        description: Erro de validação
        schema:
          type: object
          properties:
            error:
              type: string
              example: Nome e email são obrigatórios
    """
    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    if not data.get('name') or not data.get('email'):
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
    """
    Retorna um usuário específico
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Dados do usuário
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      404:
        description: Usuário não encontrado
    """
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict()), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Atualiza um usuário
    ---
    tags:
      - Usuários
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário
      - in: body
        name: body
        required: true
        schema:
          id: UserUpdate
          properties:
            name:
              type: string
              example: João Silva Atualizado
              description: Novo nome do usuário
            email:
              type: string
              example: joao.novo@example.com
              description: Novo email do usuário
    responses:
      200:
        description: Usuário atualizado com sucesso
        schema:
          id: UserResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: João Silva Atualizado
            email:
              type: string
              example: joao.novo@example.com
      400:
        description: Erro de validação
        schema:
          type: object
          properties:
            error:
              type: string
              example: Email inválido
      404:
        description: Usuário não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: Usuário não encontrado
    """
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    if data.get('name'):
        user.name = data['name']
    if data.get('email'):
        # Validação de email
        if '@' not in data['email']:
            return jsonify({'error': 'Email inválido'}), 400
        user.email = data['email']
    
    return jsonify(user.to_dict()), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deleta um usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário deletado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Usuário não encontrado
    """
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    users_db = [u for u in users_db if u.id != user_id]
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Retorna todas as tarefas
    ---
    tags:
      - Tarefas
    responses:
      200:
        description: Lista de todas as tarefas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              completed:
                type: boolean
    """
    return jsonify([task.to_dict() for task in tasks_db]), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Cria uma nova tarefa
    ---
    tags:
      - Tarefas
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: TaskCreate
          required:
            - title
          properties:
            title:
              type: string
              example: Tarefa de exemplo
              description: Título da tarefa
            description:
              type: string
              example: Descrição da tarefa
              description: Descrição detalhada da tarefa
            completed:
              type: boolean
              example: false
              description: Status de conclusão da tarefa
    responses:
      201:
        description: Tarefa criada com sucesso
        schema:
          id: TaskResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: Tarefa de exemplo
            description:
              type: string
              example: Descrição da tarefa
            completed:
              type: boolean
              example: false
      400:
        description: Erro de validação
        schema:
          type: object
          properties:
            error:
              type: string
              example: Título é obrigatório
    """
    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    if not data.get('title'):
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
    """
    Retorna uma tarefa específica
    ---
    tags:
      - Tarefas
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: ID da tarefa
    responses:
      200:
        description: Dados da tarefa
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            completed:
              type: boolean
      404:
        description: Tarefa não encontrada
    """
    task = next((t for t in tasks_db if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Atualiza uma tarefa
    ---
    tags:
      - Tarefas
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: ID da tarefa
      - in: body
        name: body
        required: true
        schema:
          id: TaskUpdate
          properties:
            title:
              type: string
              example: Tarefa atualizada
              description: Novo título da tarefa
            description:
              type: string
              example: Nova descrição
              description: Nova descrição da tarefa
            completed:
              type: boolean
              example: true
              description: Novo status de conclusão
    responses:
      200:
        description: Tarefa atualizada com sucesso
        schema:
          id: TaskResponse
          type: object
          properties:
            id:
              type: integer
              example: 1
            title:
              type: string
              example: Tarefa atualizada
            description:
              type: string
              example: Nova descrição
            completed:
              type: boolean
              example: true
      404:
        description: Tarefa não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: Tarefa não encontrada
    """
    task = next((t for t in tasks_db if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    data = request.get_json(force=True, silent=True)
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    if data.get('title'):
        task.title = data['title']
    if data.get('description') is not None:
        task.description = data['description']
    if data.get('completed') is not None:
        task.completed = data['completed']
    
    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Deleta uma tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: ID da tarefa
    responses:
      200:
        description: Tarefa deletada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Tarefa não encontrada
    """
    global tasks_db
    task = next((t for t in tasks_db if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    
    tasks_db = [t for t in tasks_db if t.id != task_id]
    return jsonify({'message': 'Tarefa deletada com sucesso'}), 200


# Handler de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Requisição inválida'}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

