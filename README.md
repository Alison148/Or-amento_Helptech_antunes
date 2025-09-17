HelpTech Antunes – API FastAPI com PDF

API em FastAPI para gerar orçamentos em PDF.
Inclui endpoint POST /gerar-pdf com validação (Pydantic) e compatibilidade por GET via querystring.

✨ Recursos

🚀 FastAPI + Uvicorn

🧾 Geração de PDF com ReportLab (formato A4, margens, título, seções)

✅ Validação de entrada (Pydantic)

🧼 Arquivo temporário por requisição + limpeza automática

🌎 Compatível com acentuação (dica de fontes abaixo)

🔁 GET compatível por querystring (útil pra testar no navegador)

📦 Requisitos

Python 3.11+

Pip

(Opcional) Docker / Docker Compose

requirements.txt (exemplo):

fastapi
uvicorn[standard]
reportlab
pydantic>=2

🗂 Estrutura sugerida
.
├─ main.py                 # API FastAPI (endpoints e geração do PDF)
├─ requirements.txt        # Dependências
├─ templates/              # Templates HTML (opcional; p/ HTML→PDF futuramente)
│  └─ base.html
├─ Dockerfile              # Build da imagem
├─ docker-compose.yml      # (Opcional) Dev/Prod
└─ .dockerignore           # Ignorar arquivos no build


.dockerignore (exemplo):

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

(Opcional) Criar ambiente virtual:

python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate


Instalar dependências:

pip install -r requirements.txt


Rodar o servidor (dev):

uvicorn main:app --reload --host 0.0.0.0 --port 8000


Acessar:

Swagger: http://127.0.0.1:8000/docs

(GET compat) Gerar PDF no navegador:
http://127.0.0.1:8000/gerar-pdf?cliente=Jo%C3%A3o&servico=Troca%20de%20Tela&valor=250

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


curl:

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

2) GET (compatibilidade por querystring)
http://127.0.0.1:8000/gerar-pdf?cliente=Jo%C3%A3o&servico=Troca%20de%20Tela&valor=250


Nota: Em produção, prefira POST (corpo JSON) — facilita validação e logs.

🐳 Rodando com Docker

Dockerfile (otimizado):

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (Opcional) fontes p/ acentuação no PDF
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

# Uvicorn (simples)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Produção (opcional):
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]


Build & run:

docker build -t helptech-fastapi-pdf .
docker run --rm -p 8000:8000 helptech-fastapi-pdf

docker-compose (opcional)
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

POST /gerar-pdf → Gera e retorna o PDF (headers de download)

GET /gerar-pdf → Compatibilidade via querystring (para testes rápidos)

Modelo (POST /gerar-pdf):

{
  "cliente": "string",
  "servico": "string",
  "valor": 0.0,
  "contato": "string|null",
  "numero": "string|null",
  "observacoes": "string|null"
}


Resposta: application/pdf (arquivo com nome orcamento-<numero>.pdf ou timestamp)

📝 Dicas de PDF (acentuação)

Se notar caracteres estranhos, registre uma fonte TTF (ex.: DejaVu):

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

# depois use:
c.setFont("DejaVu", 10)


No Dockerfile acima já instalamos fonts-dejavu-core.

🧩 Próximos passos (opcionais)

HTML → PDF com WeasyPrint/wkhtmltopdf usando templates/orcamento.html (visual mais rico).

Assinatura/QR Code PIX no PDF (carregar imagem e posicionar).

Persistência (salvar orçamentos, histórico, e-mail automático com anexo).

Autenticação (API Key ou OAuth) para uso externo.

Logs e observabilidade (uvicorn/gunicorn + middleware).

⚠️ Observações

O endpoint GET é útil para testes, mas em produção prefira POST.

PDFs são gerados em diretórios temporários e limpos automaticamente após o envio.

Caso hospede atrás de um proxy (Nginx/Traefik), assegure limites de tamanho e cabeçalhos corretos.

📜 Licença

Livre uso neste projeto HelpTech Antunes. Adapte conforme sua necessidade.