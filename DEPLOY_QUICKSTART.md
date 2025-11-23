# 🚀 Deploy Rápido - Railway (5 minutos)

Este é o guia mais rápido para fazer deploy da sua aplicação.

## Passo 1: Criar Projeto no Railway (2 min)

1. Acesse: https://railway.app
2. Clique em "Login" e faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório `labfinal-devops`
6. Railway detectará automaticamente que é Python e fará o deploy!

**Pronto! Sua aplicação já está no ar! 🎉**

Você pode ver a URL da sua aplicação no dashboard do Railway.

---

## Passo 2: Configurar Deploy Automático via GitHub Actions (3 min)

Se você quiser que o deploy seja feito automaticamente via GitHub Actions:

### 2.1 Obter Token do Railway

1. No Railway, clique no seu projeto
2. Vá em **Settings** → **Tokens**
3. Clique em **New Token**
4. Dê um nome (ex: "github-actions")
5. Copie o token gerado

### 2.2 Obter Service ID

1. Ainda nas Settings do projeto
2. Vá em **General**
3. Copie o **Service ID**

### 2.3 Adicionar Secrets no GitHub

1. No seu repositório GitHub, vá em:
   - **Settings** → **Secrets and variables** → **Actions**
2. Clique em **New repository secret**
3. Adicione:
   - Nome: `RAILWAY_TOKEN`
   - Valor: Cole o token que você copiou
4. Clique em **Add secret**
5. Adicione outro:
   - Nome: `RAILWAY_SERVICE_ID`
   - Valor: Cole o Service ID que você copiou

### 2.4 Ativar Deploy no Workflow

1. Abra o arquivo `.github/workflows/ci-cd.yml`
2. Procure pela seção `# OPÇÃO 1: RAILWAY`
3. Descomente as linhas (remova os `#`):
   ```yaml
   - name: Instalar Railway CLI
     run: |
       npm install -g @railway/cli
   
   - name: Deploy para Railway
     env:
       RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
     run: |
       railway link ${{ secrets.RAILWAY_SERVICE_ID }}
       railway up --detach
   ```

### 2.5 Fazer Commit e Push

```bash
git add .github/workflows/ci-cd.yml
git commit -m "Configurar deploy automático no Railway"
git push origin main
```

**Pronto! Agora toda vez que você fizer push na branch `main`, o deploy será feito automaticamente! 🚀**

---

## ✅ Verificar Deploy

1. Vá em **Actions** no seu repositório GitHub
2. Você verá a pipeline rodando
3. Quando o job "DEPLOY Stage" completar, sua aplicação estará atualizada!

---

## 🆘 Problemas?

- **Deploy falha?** Verifique se os secrets estão corretos
- **App não inicia?** Verifique os logs no Railway
- **Erro de porta?** A Railway define automaticamente a variável `PORT`

---

**Pronto! Sua aplicação está no ar! 🎉**

Para outras opções de deploy, consulte [DEPLOY.md](DEPLOY.md)

