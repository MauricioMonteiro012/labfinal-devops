# 🚀 Guia de Deploy - DevOps Challenge

Este guia mostra como configurar o deploy da aplicação em diferentes provedores de nuvem.

## 📋 Índice

1. [Railway (Recomendado - Mais Fácil)](#railway-recomendado)
2. [Render](#render)
3. [Heroku](#heroku)
4. [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
5. [Azure App Service](#azure-app-service)

---

## 🚂 Railway (Recomendado - Mais Fácil)

**Railway é a opção mais simples e rápida para começar!**

### Passo 1: Criar conta no Railway
1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório

### Passo 2: Configurar no GitHub Actions

1. **Obter API Token do Railway:**
   - No Railway, vá em Settings → Tokens
   - Crie um novo token
   - Copie o token

2. **Adicionar Secret no GitHub:**
   - No seu repositório GitHub, vá em Settings → Secrets and variables → Actions
   - Clique em "New repository secret"
   - Nome: `RAILWAY_TOKEN`
   - Valor: Cole o token copiado

3. **Obter Service ID:**
   - No Railway, vá no seu projeto
   - Clique em Settings → General
   - Copie o "Service ID"

4. **Adicionar outro Secret:**
   - Nome: `RAILWAY_SERVICE_ID`
   - Valor: Cole o Service ID

5. **Atualizar o workflow:**
   - Descomente a seção Railway no arquivo `.github/workflows/ci-cd.yml`

### Vantagens:
- ✅ Grátis para começar
- ✅ Deploy automático via GitHub
- ✅ Muito fácil de configurar
- ✅ HTTPS automático

---

## 🎨 Render

### Passo 1: Criar conta no Render
1. Acesse [render.com](https://render.com)
2. Faça login com GitHub
3. Clique em "New +" → "Web Service"
4. Conecte seu repositório
5. Configure:
   - **Name:** seu-app-name
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

### Passo 2: Deploy via GitHub Actions (Opcional)

Render já faz deploy automático quando você faz push. Mas se quiser controlar via Actions:

1. **Obter API Key:**
   - Vá em Account Settings → API Keys
   - Crie uma nova API Key

2. **Adicionar Secrets no GitHub:**
   - `RENDER_API_KEY`: Sua API Key
   - `RENDER_SERVICE_ID`: ID do serviço (encontre na URL do serviço)

3. **Atualizar o workflow:**
   - Descomente a seção Render no arquivo `.github/workflows/ci-cd.yml`

### Vantagens:
- ✅ Plano gratuito disponível
- ✅ Deploy automático
- ✅ SSL automático

---

## 🟣 Heroku

### Passo 1: Criar app no Heroku
1. Acesse [heroku.com](https://heroku.com)
2. Faça login
3. Clique em "New" → "Create new app"
4. Escolha um nome e região

### Passo 2: Configurar no GitHub Actions

1. **Obter API Key:**
   - Vá em Account Settings → API Key
   - Reveal e copie a API Key

2. **Adicionar Secrets no GitHub:**
   - `HEROKU_API_KEY`: Sua API Key
   - `HEROKU_APP_NAME`: Nome do seu app no Heroku
   - `HEROKU_EMAIL`: Seu email do Heroku

3. **Atualizar o workflow:**
   - Descomente a seção Heroku no arquivo `.github/workflows/ci-cd.yml`

### Vantagens:
- ✅ Muito popular
- ✅ Boa documentação
- ⚠️ Plano gratuito foi descontinuado (pode ter custos)

---

## ☁️ AWS Elastic Beanstalk

### Passo 1: Criar aplicação no AWS
1. Acesse o [AWS Console](https://console.aws.amazon.com)
2. Vá em Elastic Beanstalk
3. Crie uma nova aplicação
4. Escolha Python como plataforma

### Passo 2: Configurar no GitHub Actions

1. **Criar IAM User:**
   - Vá em IAM → Users → Add user
   - Permissões: `AWSElasticBeanstalkFullAccess`
   - Crie Access Key

2. **Adicionar Secrets no GitHub:**
   - `AWS_ACCESS_KEY_ID`: Sua Access Key
   - `AWS_SECRET_ACCESS_KEY`: Sua Secret Key
   - `AWS_REGION`: Ex: `us-east-1`
   - `EB_APPLICATION_NAME`: Nome da aplicação
   - `EB_ENVIRONMENT_NAME`: Nome do ambiente

3. **Atualizar o workflow:**
   - Descomente a seção AWS no arquivo `.github/workflows/ci-cd.yml`

### Vantagens:
- ✅ Muito escalável
- ✅ Integração com outros serviços AWS
- ⚠️ Requer conhecimento de AWS
- ⚠️ Pode ter custos

---

## 🔵 Azure App Service

### Passo 1: Criar app no Azure
1. Acesse [portal.azure.com](https://portal.azure.com)
2. Crie um novo "Web App"
3. Configure:
   - Runtime stack: Python 3.11
   - Operating System: Linux

### Passo 2: Configurar no GitHub Actions

1. **Criar Service Principal:**
   ```bash
   az ad sp create-for-rbac --name "github-actions" --role contributor
   ```

2. **Adicionar Secrets no GitHub:**
   - `AZURE_WEBAPP_NAME`: Nome do seu app
   - `AZURE_CREDENTIALS`: JSON do service principal

3. **Atualizar o workflow:**
   - Descomente a seção Azure no arquivo `.github/workflows/ci-cd.yml`

### Vantagens:
- ✅ Integração com Azure
- ✅ Boa para empresas
- ⚠️ Requer conhecimento de Azure

---

## 🎯 Qual escolher?

| Provedor | Dificuldade | Custo | Recomendado para |
|----------|------------|-------|------------------|
| **Railway** | ⭐ Fácil | Grátis | Iniciantes |
| **Render** | ⭐ Fácil | Grátis | Iniciantes |
| **Heroku** | ⭐⭐ Médio | Pago* | Projetos médios |
| **AWS** | ⭐⭐⭐ Difícil | Variável | Projetos grandes |
| **Azure** | ⭐⭐⭐ Difícil | Variável | Empresas |

\* Heroku descontinuou o plano gratuito

**Recomendação:** Comece com **Railway** ou **Render** para o desafio!

---

## 📝 Checklist de Deploy

- [ ] Escolher provedor de nuvem
- [ ] Criar conta no provedor
- [ ] Obter credenciais/API keys
- [ ] Adicionar secrets no GitHub
- [ ] Descomentar seção de deploy no workflow
- [ ] Fazer push para branch `main`
- [ ] Verificar deploy no GitHub Actions
- [ ] Testar aplicação no ambiente de produção

---

## 🆘 Troubleshooting

### Deploy falha no GitHub Actions
- Verifique se os secrets estão configurados corretamente
- Verifique os logs do workflow no GitHub
- Confirme que o nome do app/serviço está correto

### Aplicação não inicia
- Verifique o `Procfile`
- Confirme que a porta está configurada corretamente (variável `PORT`)
- Verifique os logs do provedor

### Erro de dependências
- Confirme que `requirements.txt` está completo
- Verifique se todas as dependências são compatíveis

---

**Boa sorte com o deploy! 🚀**

