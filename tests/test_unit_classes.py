"""
Tipo 2: Testes Unitários de Classes e Modelos
Testa a lógica de negócio das classes User e Task
"""
import pytest
from app import User, Task


class TestUserClass:
    """Testes unitários para a classe User"""
    
    def test_user_creation(self):
        """Testa criação de instância de User"""
        user = User(1, 'Maria', 'maria@example.com')
        assert user.id == 1
        assert user.name == 'Maria'
        assert user.email == 'maria@example.com'
    
    def test_user_to_dict(self):
        """Testa conversão de User para dicionário"""
        user = User(1, 'Pedro', 'pedro@example.com')
        user_dict = user.to_dict()
        
        assert isinstance(user_dict, dict)
        assert user_dict['id'] == 1
        assert user_dict['name'] == 'Pedro'
        assert user_dict['email'] == 'pedro@example.com'
        assert len(user_dict) == 3
    
    def test_user_multiple_instances(self):
        """Testa criação de múltiplas instâncias de User"""
        user1 = User(1, 'User 1', 'user1@example.com')
        user2 = User(2, 'User 2', 'user2@example.com')
        
        assert user1.id != user2.id
        assert user1.name != user2.name
        assert user1.email != user2.email


class TestTaskClass:
    """Testes unitários para a classe Task"""
    
    def test_task_creation_default_completed(self):
        """Testa criação de Task com completed padrão False"""
        task = Task(1, 'Tarefa 1', 'Descrição')
        assert task.id == 1
        assert task.title == 'Tarefa 1'
        assert task.description == 'Descrição'
        assert task.completed is False
    
    def test_task_creation_with_completed(self):
        """Testa criação de Task com completed True"""
        task = Task(1, 'Tarefa 1', 'Descrição', completed=True)
        assert task.completed is True
    
    def test_task_to_dict(self):
        """Testa conversão de Task para dicionário"""
        task = Task(1, 'Tarefa Teste', 'Descrição Teste', completed=True)
        task_dict = task.to_dict()
        
        assert isinstance(task_dict, dict)
        assert task_dict['id'] == 1
        assert task_dict['title'] == 'Tarefa Teste'
        assert task_dict['description'] == 'Descrição Teste'
        assert task_dict['completed'] is True
        assert len(task_dict) == 4
    
    def test_task_state_changes(self):
        """Testa mudanças de estado da Task"""
        task = Task(1, 'Tarefa', 'Descrição', completed=False)
        assert task.completed is False
        
        task.completed = True
        assert task.completed is True
        
        task.title = 'Tarefa Atualizada'
        assert task.title == 'Tarefa Atualizada'
    
    def test_task_empty_description(self):
        """Testa criação de Task sem descrição"""
        task = Task(1, 'Tarefa', '')
        assert task.description == ''
        task_dict = task.to_dict()
        assert task_dict['description'] == ''


class TestDataIntegrity:
    """Testes de integridade de dados"""
    
    def test_user_data_consistency(self):
        """Testa consistência dos dados do User"""
        user = User(10, 'Test User', 'test@example.com')
        user_dict = user.to_dict()
        
        # Verificar que todos os campos estão presentes
        required_fields = ['id', 'name', 'email']
        for field in required_fields:
            assert field in user_dict
    
    def test_task_data_consistency(self):
        """Testa consistência dos dados da Task"""
        task = Task(5, 'Test Task', 'Test Description', completed=False)
        task_dict = task.to_dict()
        
        # Verificar que todos os campos estão presentes
        required_fields = ['id', 'title', 'description', 'completed']
        for field in required_fields:
            assert field in task_dict
        
        # Verificar tipos
        assert isinstance(task_dict['id'], int)
        assert isinstance(task_dict['title'], str)
        assert isinstance(task_dict['description'], str)
        assert isinstance(task_dict['completed'], bool)

