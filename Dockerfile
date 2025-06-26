# Dockerfile para FastAPI + Poetry + Gunicorn/Uvicorn
FROM python:3.13-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y build-essential libffi-dev libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock README.md ./

# Instala dependências (sem dev)
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copia o restante da aplicação
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a aplicação em produção
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4"]
