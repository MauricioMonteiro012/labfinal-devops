# Use Python 3.11 como imagem base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta (Render usa variável de ambiente PORT)
EXPOSE $PORT

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Comando para executar a aplicação com gunicorn (produção)
# Render injeta a variável PORT automaticamente
# Usa sh -c para permitir expansão da variável PORT
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 app:app"


