# Usar imagem oficial do Python 3.11 slim
FROM python:3.11-slim AS base

# Variáveis de ambiente para não criar .pyc e melhorar logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências primeiro (cache mais eficiente)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar apenas o código da aplicação
COPY . .

# Expor a porta padrão
EXPOSE 8000

# Comando de inicialização (produção: workers > 1)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
