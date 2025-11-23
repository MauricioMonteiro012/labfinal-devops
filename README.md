# Desafio Final: Pipeline DevOps

Este projeto implementa uma pipeline CI/CD completa usando GitHub Actions, seguindo os requisitos do desafio final de DevOps.

## 📋 Estrutura do Projeto

```
labfinal-devops/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── tests/                 # Testes unitários
│   ├── test_unit_api.py           # Tipo 1: Testes de Endpoints API
│   ├── test_unit_classes.py       # Tipo 2: Testes de Classes/Modelos
│   └── test_unit_validation.py    # Tipo 3: Testes de Validação
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # Pipeline CI/CD
└── README.md
```

## 🚀 Pipeline CI/CD

A pipeline está dividida em 3 estágios principais:

### 1. BUILD Stage
- Verifica o código-fonte
- Configura o ambiente Python
- Instala dependências
- Valida a estrutura do projeto
- Prepara artefatos para execução

### 2. TEST Stage
- Executa 3 tipos diferentes de testes unitários:
  - **Tipo 1**: Testes de Endpoints da API (`test_unit_api.py`)
  - **Tipo 2**: Testes de Classes e Modelos (`test_unit_classes.py`)
  - **Tipo 3**: Testes de Validação e Regras de Negócio (`test_unit_validation.py`)
- Gera relatório de cobertura de código
- Valida qualidade do código

### 3. DEPLOY Stage
- Executa apenas na branch `main` ou `master`
- Prepara a aplicação para deploy
- Realiza deploy para o ambiente de produção
- Configurável para diferentes provedores de nuvem

## 🧪 Testes Unitários

O projeto implementa **3 tipos diferentes de testes unitários**:

### Tipo 1: Testes de Endpoints da API
- Testa cada endpoint individualmente
- Valida códigos de status HTTP
- Testa criação, leitura, atualização e deleção
- Cobre casos de sucesso e erro

### Tipo 2: Testes de Classes e Modelos
- Testa a lógica de negócio das classes `User` e `Task`
- Valida criação de instâncias
- Testa conversão para dicionários
- Verifica integridade de dados

### Tipo 3: Testes de Validação e Regras de Negócio
- Testa validações de entrada (email, campos obrigatórios)
- Valida regras de negócio (auto-incremento de IDs)
- Testa tratamento de erros (404, 400)
- Cobre casos extremos e edge cases

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação
- **Flask**: Framework web
- **pytest**: Framework de testes
- **pytest-cov**: Cobertura de código
- **GitHub Actions**: Automação CI/CD
- **Gunicorn**: Servidor WSGI para produção

## 📦 Instalação e Execução Local

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd labfinal-devops
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute os testes:
```bash
pytest tests/ -v
```

4. Execute a aplicação:
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 🧪 Executar Testes

```bash
# Todos os testes
pytest tests/ -v

# Testes com cobertura
pytest tests/ --cov=app --cov-report=html

# Teste específico
pytest tests/test_unit_api.py -v
```

## 🌐 Endpoints da API

- `GET /` - Página inicial
- `GET /health` - Health check
- `GET /users` - Lista todos os usuários
- `POST /users` - Cria um novo usuário
- `GET /users/<id>` - Busca um usuário específico
- `GET /tasks` - Lista todas as tarefas
- `POST /tasks` - Cria uma nova tarefa
- `PUT /tasks/<id>` - Atualiza uma tarefa
- `DELETE /tasks/<id>` - Deleta uma tarefa

## ☁️ Deploy em Nuvem

A pipeline está configurada para deploy, mas requer configuração adicional baseada no provedor escolhido.

### 📖 Guia Completo de Deploy

**Consulte o arquivo [DEPLOY.md](DEPLOY.md) para instruções detalhadas de cada provedor!**

### Opções de Provedores Disponíveis:
- **🚂 Railway** (Recomendado - Mais fácil e grátis)
- **🎨 Render** (Fácil e grátis)
- **🟣 Heroku** (Popular, pode ter custos)
- **☁️ AWS** (Elastic Beanstalk - Escalável)
- **🔵 Azure** (App Service - Para empresas)

### Configuração Rápida (Railway - Recomendado):

1. **Criar conta no Railway:**
   - Acesse [railway.app](https://railway.app)
   - Faça login com GitHub
   - Crie um novo projeto conectando seu repositório

2. **Configurar Secrets no GitHub:**
   - Vá em Settings → Secrets and variables → Actions
   - Adicione:
     - `RAILWAY_TOKEN` (obtenha em Settings → Tokens no Railway)
     - `RAILWAY_SERVICE_ID` (obtenha em Settings → General no Railway)

3. **Atualizar o Workflow:**
   - Abra `.github/workflows/ci-cd.yml`
   - Descomente a seção "OPÇÃO 1: RAILWAY"

4. **Fazer Deploy:**
   - Faça push para a branch `main` ou `master`
   - O deploy será executado automaticamente!

**Para outros provedores, consulte [DEPLOY.md](DEPLOY.md)**

## 📊 Status da Pipeline

A pipeline é executada automaticamente em:
- Push para `main`, `master` ou `develop`
- Pull Requests para `main` ou `master`

Você pode verificar o status no GitHub em: **Actions** → **CI/CD Pipeline**

## 📝 Notas

- Os testes são executados em paralelo nos 3 tipos diferentes
- A cobertura de código é gerada e disponibilizada como artefato
- O deploy só ocorre na branch principal após testes bem-sucedidos
- A aplicação usa armazenamento em memória (reinicia a cada execução)

## 🎯 Requisitos Atendidos

✅ Pipeline CI/CD completa com GitHub Actions  
✅ 3 estágios: BUILD, TEST, DEPLOY  
✅ 3 tipos diferentes de testes unitários  
✅ Cobertura de código  
✅ Configuração para deploy em qualquer provedor de nuvem  
✅ Documentação completa  

## 👤 Autor

Projeto desenvolvido para o Desafio Final de DevOps.

---

**Made with ❤️ for DevOps Challenge**

