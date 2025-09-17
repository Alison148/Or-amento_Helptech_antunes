HelpTech Antunes – API FastAPI com PDF

API em FastAPI para gerar orçamentos em PDF.
Inclui endpoint POST /gerar-pdf com validação (Pydantic) e compatibilidade via GET querystring para testes rápidos.

✨ Recursos

🚀 FastAPI + Uvicorn

🧾 Geração de PDF com ReportLab (formato A4, margens, título e seções)

✅ Validação de entrada com Pydantic

🧼 Arquivos temporários por requisição + limpeza automática

🌎 Compatível com acentuação UTF-8 (via fontes extras)

🔁 Suporte a GET (querystring) para testes diretos no navegador

📦 Requisitos

Python 3.11+

Pip

(Opcional) Docker / Docker Compose

requirements.txt (exemplo)
fastapi
uvicorn[standard]
reportlab
pydantic>=2

🗂 Estrutura sugerida
.
├─ main.py                 # API FastAPI (endpoints e geração do PDF)
├─ requirements.txt        # Dependências
├─ templates/              # Templates HTML (opcional, para HTML→PDF futuramente)
│  └─ base.html
├─ Dockerfile              # Build da imagem
├─ docker-compose.yml      # (opcional) Configuração Dev/Prod
└─ .dockerignore           # Ignorar arquivos no build

.dockerignore (exemplo)
__pycache__/
*.pyc
*.pyo
*.pyd
*.sqlite3
.env
.git
.gitignore
.vscode
.idea
*.log

🏃 Como rodar (sem Docker)
Criar ambiente virtual (opcional)
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

Instalar dependências
pip install -r requirements.txt

Rodar servidor (modo dev)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Acessar no navegador

Swagger: http://127.0.0.1:8000/docs

Gerar PDF (GET):

http://127.0.0.1:8000/gerar-pdf?cliente=João&servico=Troca%20de%20Tela&valor=250

🧪 Exemplos de uso
1) POST (recomendado)

Payload (JSON):

{
  "cliente": "João Silva",
  "servico": "Troca de tela – Moto G",
  "valor": 250.0,
  "contato": "11 90000-0000",
  "numero": "2025-0001",
  "observacoes": "Peça com garantia de 90 dias."
}


cURL:

curl -X POST "http://localhost:8000/gerar-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "João Silva",
    "servico": "Troca de tela – Moto G",
    "valor": 250.0,
    "contato": "11 90000-0000",
    "numero": "2025-0001",
    "observacoes": "Peça com garantia de 90 dias."
  }' --output orcamento.pdf

2) GET (compatibilidade)
http://127.0.0.1:8000/gerar-pdf?cliente=João&servico=Troca%20de%20Tela&valor=250


⚠️ Nota: Em produção prefira POST — facilita logs e validações.

🐳 Docker
Dockerfile (otimizado)
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala fontes (acentuação no PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Dev (simples)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Produção (opcional)
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]

Build & Run
docker build -t helptech-fastapi-pdf .
docker run --rm -p 8000:8000 helptech-fastapi-pdf

docker-compose.yml (opcional)
version: "3.9"
services:
  api:
    build: .
    image: helptech-fastapi-pdf:latest
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

🔗 Endpoints

GET / → Healthcheck simples

POST /gerar-pdf → Gera e retorna o PDF (recomendado)

GET /gerar-pdf → Compatibilidade via querystring (para testes rápidos)

Modelo (POST /gerar-pdf)
{
  "cliente": "string",
  "servico": "string",
  "valor": 0.0,
  "contato": "string|null",
  "numero": "string|null",
  "observacoes": "string|null"
}


📄 Resposta: application/pdf
Arquivo nomeado orcamento-<numero>.pdf ou com timestamp.

📝 Dicas de PDF (acentuação)

Se notar problemas com acentos, registre fonte TTF no main.py:

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


E depois:

c.setFont("DejaVu", 10)


No Dockerfile já instalamos fonts-dejavu-core.

🧩 Próximos passos (opcionais)

HTML → PDF com WeasyPrint/wkhtmltopdf usando templates/orcamento.html.

Assinatura digital ou QR Code PIX no PDF.

Persistência: salvar orçamentos, histórico, envio automático por e-mail.

Autenticação (API Key / OAuth).

Logs e observabilidade (uvicorn/gunicorn + middleware).

⚠️ Observações

O endpoint GET é útil para testes, mas POST é recomendado em produção.

PDFs são gerados em diretórios temporários e apagados após envio.

Se usar proxy reverso (Nginx/Traefik), configure limites e headers corretamente.

📜 Licença

Uso livre no projeto HelpTech Antunes.
Adapte e expanda conforme necessidade.