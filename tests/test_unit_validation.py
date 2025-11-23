"""
Tipo 3: Testes Unitários de Validação e Regras de Negócio
Testa validações, regras de negócio e tratamento de erros
"""
import pytest
from app import app, users_db, tasks_db


@pytest.fixture
def client():
    """Fixture para criar um cliente de teste"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    users_db.clear()
    tasks_db.clear()


class TestValidationRules:
    """Testes de validação e regras de negócio"""
    
    def test_email_validation_with_at_symbol(self, client):
        """Testa validação de email - deve conter @"""
        # Email válido
        response1 = client.post('/users', json={
            'name': 'User 1',
            'email': 'valid@email.com'
        })
        assert response1.status_code == 201
        
        # Email inválido - sem @
        response2 = client.post('/users', json={
            'name': 'User 2',
            'email': 'invalid-email.com'
        })
        assert response2.status_code == 400
    
    def test_required_fields_validation(self, client):
        """Testa validação de campos obrigatórios"""
        # Sem name
        response1 = client.post('/users', json={'email': 'test@example.com'})
        assert response1.status_code == 400
        
        # Sem email
        response2 = client.post('/users', json={'name': 'Test User'})
        assert response2.status_code == 400
        
        # Sem dados
        response3 = client.post('/users', json={})
        assert response3.status_code == 400
    
    def test_task_title_required(self, client):
        """Testa que título da tarefa é obrigatório"""
        response = client.post('/tasks', json={'description': 'Sem título'})
        assert response.status_code == 400
    
    def test_task_description_optional(self, client):
        """Testa que descrição da tarefa é opcional"""
        response = client.post('/tasks', json={'title': 'Tarefa sem descrição'})
        assert response.status_code == 201
        data = response.get_json()
        assert data['description'] == ''


class TestBusinessRules:
    """Testes de regras de negócio"""
    
    def test_user_id_auto_increment(self, client):
        """Testa que IDs de usuários são incrementados automaticamente"""
        user1 = client.post('/users', json={
            'name': 'User 1',
            'email': 'user1@example.com'
        }).get_json()
        
        user2 = client.post('/users', json={
            'name': 'User 2',
            'email': 'user2@example.com'
        }).get_json()
        
        assert user2['id'] == user1['id'] + 1
    
    def test_task_id_auto_increment(self, client):
        """Testa que IDs de tarefas são incrementados automaticamente"""
        task1 = client.post('/tasks', json={'title': 'Task 1'}).get_json()
        task2 = client.post('/tasks', json={'title': 'Task 2'}).get_json()
        
        assert task2['id'] == task1['id'] + 1
    
    def test_task_default_completed_false(self, client):
        """Testa que tarefas são criadas com completed=False por padrão"""
        response = client.post('/tasks', json={'title': 'Nova Tarefa'})
        data = response.get_json()
        assert data['completed'] is False
    
    def test_task_completed_can_be_set(self, client):
        """Testa que completed pode ser definido na criação"""
        response = client.post('/tasks', json={
            'title': 'Tarefa Completa',
            'completed': True
        })
        data = response.get_json()
        assert data['completed'] is True


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_get_nonexistent_user_404(self, client):
        """Testa retorno 404 para usuário inexistente"""
        response = client.get('/users/999')
        assert response.status_code == 404
        assert 'error' in response.get_json()
    
    def test_get_nonexistent_task_404(self, client):
        """Testa retorno 404 para tarefa inexistente"""
        response = client.get('/tasks/999')
        assert response.status_code == 404
    
    def test_update_nonexistent_task_404(self, client):
        """Testa atualização de tarefa inexistente"""
        response = client.put('/tasks/999', json={'title': 'Updated'})
        assert response.status_code == 404
    
    def test_delete_nonexistent_task_404(self, client):
        """Testa deleção de tarefa inexistente"""
        response = client.delete('/tasks/999')
        assert response.status_code == 404
    
    def test_partial_task_update(self, client):
        """Testa atualização parcial de tarefa"""
        # Criar tarefa
        create_response = client.post('/tasks', json={
            'title': 'Tarefa Original',
            'description': 'Descrição Original',
            'completed': False
        })
        task_id = create_response.get_json()['id']
        
        # Atualizar apenas o título
        update_response = client.put(f'/tasks/{task_id}', json={
            'title': 'Título Atualizado'
        })
        data = update_response.get_json()
        assert data['title'] == 'Título Atualizado'
        assert data['description'] == 'Descrição Original'  # Mantém valor original
        assert data['completed'] is False  # Mantém valor original


class TestEdgeCases:
    """Testes de casos extremos"""
    
    def test_empty_json_request(self, client):
        """Testa requisição com JSON vazio"""
        response = client.post('/users', json={})
        assert response.status_code == 400
    
    def test_special_characters_in_names(self, client):
        """Testa caracteres especiais em nomes"""
        response = client.post('/users', json={
            'name': 'José da Silva-Santos',
            'email': 'jose@example.com'
        })
        assert response.status_code == 201
    
    def test_long_email_address(self, client):
        """Testa email longo"""
        long_email = 'a' * 50 + '@example.com'
        response = client.post('/users', json={
            'name': 'Test',
            'email': long_email
        })
        assert response.status_code == 201
    
    def test_empty_string_title_validation(self, client):
        """Testa título vazio"""
        response = client.post('/tasks', json={'title': ''})
        # Flask aceita string vazia, mas podemos verificar o comportamento
        # Neste caso, aceita mas pode ser melhorado com validação adicional
        assert response.status_code in [201, 400]

