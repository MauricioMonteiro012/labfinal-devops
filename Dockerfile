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

# Expõe a porta 5000 (padrão)
EXPOSE 5000

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Comando para executar a aplicação com gunicorn (produção)
# Usa a variável PORT ou padrão 5000
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 120 app:app"


