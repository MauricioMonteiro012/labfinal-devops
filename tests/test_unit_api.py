"""
Tipo 1: Testes Unitários de Endpoints da API
Testa cada endpoint individualmente com diferentes cenários
"""
import pytest
from app import app, users_db, tasks_db, User, Task


@pytest.fixture
def client():
    """Fixture para criar um cliente de teste"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Limpar dados após cada teste
    users_db.clear()
    tasks_db.clear()


class TestAPIEndpoints:
    """Testes unitários para endpoints da API"""
    
    def test_home_endpoint(self, client):
        """Testa o endpoint raiz"""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'running'
        assert 'version' in data
    
    def test_health_check(self, client):
        """Testa o endpoint de health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_create_user_success(self, client):
        """Testa criação de usuário com sucesso"""
        response = client.post('/users', json={
            'name': 'João Silva',
            'email': 'joao@example.com'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'João Silva'
        assert data['email'] == 'joao@example.com'
        assert 'id' in data
    
    def test_create_user_missing_fields(self, client):
        """Testa criação de usuário sem campos obrigatórios"""
        response = client.post('/users', json={'name': 'João'})
        assert response.status_code == 400
    
    def test_create_user_invalid_email(self, client):
        """Testa criação de usuário com email inválido"""
        response = client.post('/users', json={
            'name': 'João',
            'email': 'email-invalido'
        })
        assert response.status_code == 400
    
    def test_get_users_empty(self, client):
        """Testa listagem de usuários quando não há usuários"""
        response = client.get('/users')
        assert response.status_code == 200
        assert response.get_json() == []
    
    def test_get_user_not_found(self, client):
        """Testa busca de usuário inexistente"""
        response = client.get('/users/999')
        assert response.status_code == 404
    
    def test_create_and_get_task(self, client):
        """Testa criação e busca de tarefa"""
        # Criar tarefa
        create_response = client.post('/tasks', json={
            'title': 'Tarefa de teste',
            'description': 'Descrição da tarefa'
        })
        assert create_response.status_code == 201
        task_id = create_response.get_json()['id']
        
        # Buscar tarefas
        get_response = client.get('/tasks')
        assert get_response.status_code == 200
        tasks = get_response.get_json()
        assert len(tasks) == 1
        assert tasks[0]['title'] == 'Tarefa de teste'
    
    def test_update_task(self, client):
        """Testa atualização de tarefa"""
        # Criar tarefa
        create_response = client.post('/tasks', json={
            'title': 'Tarefa original',
            'completed': False
        })
        task_id = create_response.get_json()['id']
        
        # Atualizar tarefa
        update_response = client.put(f'/tasks/{task_id}', json={
            'title': 'Tarefa atualizada',
            'completed': True
        })
        assert update_response.status_code == 200
        data = update_response.get_json()
        assert data['title'] == 'Tarefa atualizada'
        assert data['completed'] is True
    
    def test_delete_task(self, client):
        """Testa deleção de tarefa"""
        # Criar tarefa
        create_response = client.post('/tasks', json={'title': 'Tarefa para deletar'})
        task_id = create_response.get_json()['id']
        
        # Deletar tarefa
        delete_response = client.delete(f'/tasks/{task_id}')
        assert delete_response.status_code == 200
        
        # Verificar que foi deletada
        get_response = client.get('/tasks')
        assert len(get_response.get_json()) == 0

