# 🎨 Configuração do Render - Guia Rápido

## Problema: Render não encontra o Dockerfile

Se o Render não está encontrando o Dockerfile, siga estes passos:

## ✅ Solução 1: Usar render.yaml (Recomendado)

1. **O arquivo `render.yaml` já está no repositório** - ele configura tudo automaticamente

2. **No Render Dashboard:**
   - Vá em "New +" → "Blueprint"
   - Conecte seu repositório GitHub
   - O Render detectará automaticamente o `render.yaml`
   - Clique em "Apply"

## ✅ Solução 2: Configuração Manual

Se preferir configurar manualmente:

1. **Criar Web Service:**
   - Vá em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Escolha a branch `main`

2. **Configurações Importantes:**
   - **Name:** labfinal-devops (ou o nome que preferir)
   - **Environment:** Docker
   - **Dockerfile Path:** `Dockerfile` (deixe em branco ou coloque apenas `Dockerfile`)
   - **Docker Context:** `.` (ponto, significa raiz do projeto)
   - **Plan:** Free

3. **Variáveis de Ambiente (opcional, mas recomendado):**
   - `FLASK_APP` = `app.py`
   - `PYTHONUNBUFFERED` = `1`

4. **Clique em "Create Web Service"**

## ✅ Solução 3: Usar Procfile (Alternativa)

Se o Dockerfile ainda não funcionar, você pode usar o Procfile:

1. **No Render, configure:**
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

2. **O Render usará o Procfile automaticamente**

## 🔍 Verificações

1. **Certifique-se de que o Dockerfile está na raiz:**
   ```bash
   ls -la Dockerfile
   ```

2. **Verifique se o Dockerfile está no Git:**
   ```bash
   git ls-files | grep Dockerfile
   ```

3. **Se não estiver, adicione:**
   ```bash
   git add Dockerfile
   git commit -m "Adicionar Dockerfile"
   git push
   ```

## 📝 Notas Importantes

- O Render precisa que o Dockerfile esteja na **raiz do repositório**
- O Dockerfile deve estar **commitado no Git** (não apenas local)
- Se usar `render.yaml`, o Render detecta automaticamente
- O Render injeta a variável `PORT` automaticamente - não precisa configurar

## 🚨 Erro Comum: "Dockerfile not found"

**Causa:** O Dockerfile não está na raiz ou não foi commitado

**Solução:**
1. Verifique se está na raiz: `git ls-files | grep Dockerfile`
2. Se não aparecer, faça: `git add Dockerfile && git commit -m "Add Dockerfile" && git push`
3. No Render, certifique-se que "Dockerfile Path" está como `Dockerfile` (sem caminho)

## 📞 Suporte

Se ainda não funcionar:
1. Verifique os logs do build no Render
2. Certifique-se que o repositório está conectado corretamente
3. Tente usar o `render.yaml` que já está configurado

